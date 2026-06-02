import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="深达 / 广达 出单分析", page_icon="💅", layout="centered")

st.title("💅 NailVesta 深达 / 广达 出单分析")
st.caption("上传两个文件，自动计算深达出单 vs 广达出单的人数与占比")


def clean_handle(h):
    """清洗深度达人 handle：
    - 去掉全角括号备注，如 inessaakin（改名inessaak） -> inessaakin
    - 去掉结尾的 -数字（不同视频后缀），如 lexlifestyle_01-2 -> lexlifestyle_01
    - 转小写、去首尾空格
    """
    if pd.isna(h):
        return None
    s = str(h).strip()
    s = re.sub(r"（.*?）", "", s)   # 全角括号备注
    s = re.sub(r"\(.*?\)", "", s)   # 半角括号备注
    s = re.sub(r"-\d+$", "", s)      # 结尾 -数字
    s = s.strip().lower()
    return s or None


def norm_username(u):
    if pd.isna(u):
        return None
    s = str(u).strip().lower()
    return s or None


def read_table(uploaded):
    """根据后缀读取 xlsx/xls/csv。"""
    name = (uploaded.name or "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded)
    return pd.read_excel(uploaded)


with st.sidebar:
    st.header("📂 上传文件")
    deep_file = st.file_uploader(
        "深度达人 List（NailVesta_深度达人List.xlsx / .csv）",
        type=["xlsx", "xls", "csv"],
        key="deep",
    )
    cre_file = st.file_uploader(
        "Creator List（Creator_List_*.xlsx / .csv）",
        type=["xlsx", "xls", "csv"],
        key="cre",
    )

if not deep_file or not cre_file:
    st.info("请在左侧上传两个文件后开始分析。")
    st.stop()

# ---- 读取深度达人名单 ----
deep_df = read_table(deep_file)
if "handle" not in deep_df.columns:
    st.error(f"深度达人文件中没有找到 'handle' 列。现有列：{list(deep_df.columns)}")
    st.stop()

deep_df["_clean"] = deep_df["handle"].apply(clean_handle)
deep_set = set(deep_df["_clean"].dropna())

# ---- 读取 Creator List，过滤 Affiliate GMV != 0 ----
cre_df = read_table(cre_file)
if "Creator username" not in cre_df.columns or "Affiliate GMV" not in cre_df.columns:
    st.error(
        f"Creator 文件需要 'Creator username' 和 'Affiliate GMV' 列。现有列：{list(cre_df.columns)}"
    )
    st.stop()

cre_df["_uname"] = cre_df["Creator username"].apply(norm_username)
cre_df["_gmv"] = pd.to_numeric(cre_df["Affiliate GMV"], errors="coerce").fillna(0)
active_df = cre_df[(cre_df["_gmv"] != 0) & (cre_df["_uname"].notna())]
active_set = set(active_df["_uname"])

# ---- 分类 ----
deep_orders = active_set & deep_set        # 深达出单
guang_orders = active_set - deep_set        # 广达出单（出单但不在深度名单）
total_active = len(active_set)

n_deep = len(deep_orders)
n_guang = len(guang_orders)

pct_deep = n_deep / total_active * 100 if total_active else 0
pct_guang = n_guang / total_active * 100 if total_active else 0

# ---- 展示 ----
st.subheader("📊 结果")

c1, c2, c3 = st.columns(3)
c1.metric("出单达人总数", total_active)
c2.metric("深达出单", n_deep, f"{pct_deep:.1f}%")
c3.metric("广达出单", n_guang, f"{pct_guang:.1f}%")

st.divider()

summary = pd.DataFrame(
    {
        "类别": ["深达出单", "广达出单", "合计"],
        "人数": [n_deep, n_guang, total_active],
        "占比": [f"{pct_deep:.1f}%", f"{pct_guang:.1f}%", "100.0%"],
    }
)
st.table(summary)

st.bar_chart(
    pd.DataFrame({"人数": [n_deep, n_guang]}, index=["深达出单", "广达出单"])
)

st.caption(
    f"深度达人名单去重后共 {len(deep_set)} 位；Creator List 中 Affiliate GMV ≠ 0 的达人共 {total_active} 位。"
)

# ---- 出单达人 Top 10（按 GMV）----
st.divider()
st.subheader("🏆 出单达人 Top 10（按 Affiliate GMV）")

# 同一达人若有多行，先按 username 聚合 GMV，再降序取前 10
gmv_by_user = active_df.groupby("_uname", as_index=False)["_gmv"].sum()
gmv_by_user["分类"] = gmv_by_user["_uname"].apply(
    lambda u: "深达" if u in deep_set else "广达"
)
gmv_by_user = gmv_by_user.sort_values("_gmv", ascending=False).reset_index(drop=True)

TOP_N = 10
top_n = gmv_by_user.head(TOP_N).copy()
top_n.insert(0, "排名", range(1, len(top_n) + 1))

total_gmv = float(cre_df["_gmv"].sum())          # 全部 Affiliate GMV
top_gmv = float(top_n["_gmv"].sum())             # Top10 合计 GMV
n_top = len(top_n)
top_deep = int((top_n["分类"] == "深达").sum())   # Top10 中深达数量

pct_top_in_top = top_deep / n_top * 100 if n_top else 0          # 深达 ÷ Top10
pct_top_gmv = top_gmv / total_gmv * 100 if total_gmv else 0      # Top10 GMV ÷ 总 GMV

# 表格（用归一化后的小写 username 展示，与下方名单口径一致）
show_top = top_n.rename(
    columns={"_uname": "Creator username", "_gmv": "Affiliate GMV"}
)[["排名", "Creator username", "Affiliate GMV", "分类"]]
st.table(show_top)

t1, t2 = st.columns(2)
t1.metric("Top10 中深达", f"{top_deep}/{n_top}", f"{pct_top_in_top:.1f}%")
t2.metric("Top10 GMV 占总 GMV", f"{pct_top_gmv:.1f}%")

st.caption(
    f"Top {n_top} 中深达 {top_deep} 位，占 Top{n_top} 的 {pct_top_in_top:.1f}%；"
    f"Top{n_top} 合计 GMV {top_gmv:,.0f}，占总 GMV（{total_gmv:,.0f}）的 {pct_top_gmv:.1f}%。"
)

# ---- 明细 ----
with st.expander("查看 深达出单 名单"):
    st.write(sorted(deep_orders))

with st.expander("查看 广达出单 名单（出单但不在深度名单）"):
    st.write(sorted(guang_orders))

# ---- 下载 ----
detail = active_df.assign(
    分类=active_df["_uname"].apply(lambda u: "深达出单" if u in deep_set else "广达出单")
)[["Creator username", "Affiliate GMV", "分类"]]

st.download_button(
    "⬇️ 下载出单达人分类明细 (CSV)",
    detail.to_csv(index=False).encode("utf-8-sig"),
    "出单达人分类明细.csv",
    "text/csv",
)
