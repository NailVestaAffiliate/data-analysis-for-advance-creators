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
    if s in ("", "nan", "none", "--", "-"):
        return None
    return s


def read_table(uploaded):
    """根据后缀读取 xlsx/xls/csv。"""
    name = (uploaded.name or "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded)
    return pd.read_excel(uploaded)


def to_number(series):
    """把可能带 $ ￥ 千分位逗号 空格的金额/数量列转成数字。
    例：'$365.84' -> 365.84，'1,234.56' -> 1234.56，'(12)' -> -12。
    纯数字列也安全（原样转换）。无法解析的置 0。
    """
    s = series.astype(str).str.strip()
    s = s.str.replace(r"^\((.*)\)$", r"-\1", regex=True)   # 会计负数 (12) -> -12
    s = s.str.replace(r"[,，$￥\s]", "", regex=True)        # 去符号/千分位/空格
    return pd.to_numeric(s, errors="coerce").fillna(0)


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
cre_df["_gmv"] = to_number(cre_df["Affiliate GMV"])
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
    f"Top{n_top} 合计 GMV {top_gmv:,.2f}，占总 GMV（{total_gmv:,.2f}）的 {pct_top_gmv:.1f}%。"
)

# ---- 人均指标 & 深达 vs 广达 GMV ----
st.divider()
st.subheader("📈 人均指标 & 深达 vs 广达 GMV")

# 自动探测"出单数/订单数"列（用于人均出单）
order_col = None
for col in cre_df.columns:
    name = str(col).strip().lower()
    if any(kw in name for kw in ["order", "出单", "订单", "sold"]):
        order_col = col
        break

# 每位出单达人聚合：GMV（复用前面已算的 gmv_by_user），按需并入出单数
user_agg = gmv_by_user.copy()  # 含 _uname, _gmv, 分类
if order_col is not None:
    cre_df["_orders"] = to_number(cre_df[order_col])
    orders_by_user = (
        cre_df[(cre_df["_gmv"] != 0) & (cre_df["_uname"].notna())]
        .groupby("_uname", as_index=False)["_orders"].sum()
    )
    user_agg = user_agg.merge(orders_by_user, on="_uname", how="left")
    user_agg["_orders"] = user_agg["_orders"].fillna(0)


def group_row(label, sub):
    n = len(sub)
    gmv = float(sub["_gmv"].sum())
    pct = gmv / total_gmv * 100 if total_gmv else 0
    row = {
        "类别": label,
        "出单人数": n,
        "总GMV": f"{gmv:,.2f}",
        "GMV占比": f"{pct:.1f}%",
        "人均GMV": f"{gmv / n:,.2f}" if n else "—",
    }
    if order_col is not None:
        orders = float(sub["_orders"].sum())
        row["总出单数"] = f"{orders:,.0f}"
        row["人均出单"] = f"{orders / n:,.1f}" if n else "—"
    return row


rows = [
    group_row("深达", user_agg[user_agg["分类"] == "深达"]),
    group_row("广达", user_agg[user_agg["分类"] == "广达"]),
]

# 未归类：有 GMV 但无 username 的行，无法判定深达/广达。
# 用"平台总额 − 可归类额"反推，确保与后台总额完全对账。
classified_gmv = float(user_agg["_gmv"].sum())
unclassified_gmv = max(total_gmv - classified_gmv, 0.0)
unclassified_mask = (cre_df["_gmv"] != 0) & (cre_df["_uname"].isna())
unclassified_n = int(unclassified_mask.sum())

if unclassified_gmv > 0.005 or unclassified_n > 0:
    urow = {
        "类别": "未归类（无 username）",
        "出单人数": unclassified_n,
        "总GMV": f"{unclassified_gmv:,.2f}",
        "GMV占比": f"{unclassified_gmv / total_gmv * 100:.1f}%" if total_gmv else "—",
        "人均GMV": "—",
    }
    if order_col is not None:
        urow["总出单数"] = f"{float(cre_df.loc[unclassified_mask, '_orders'].sum()):,.0f}"
        urow["人均出单"] = "—"
    rows.append(urow)

# 合计 = 平台总额（对齐后台），占比 100%
trow = {
    "类别": "合计",
    "出单人数": len(user_agg) + unclassified_n,
    "总GMV": f"{total_gmv:,.2f}",
    "GMV占比": "100.0%",
    "人均GMV": "",
}
if order_col is not None:
    tot_orders = float(user_agg["_orders"].sum()) + float(cre_df.loc[unclassified_mask, "_orders"].sum())
    trow["总出单数"] = f"{tot_orders:,.0f}"
    trow["人均出单"] = ""
rows.append(trow)

metrics_df = pd.DataFrame(rows)
st.table(metrics_df)

# 深达 vs 广达 GMV 占比（突出展示）
deep_gmv = float(user_agg.loc[user_agg["分类"] == "深达", "_gmv"].sum())
guang_gmv = float(user_agg.loc[user_agg["分类"] == "广达", "_gmv"].sum())
g1, g2 = st.columns(2)
g1.metric("深达 GMV", f"{deep_gmv:,.2f}",
          f"{deep_gmv / total_gmv * 100:.1f}%" if total_gmv else "—")
g2.metric("广达 GMV", f"{guang_gmv:,.2f}",
          f"{guang_gmv / total_gmv * 100:.1f}%" if total_gmv else "—")

recon = (
    f"总 GMV {total_gmv:,.2f}（对齐后台）＝ 可归类 {classified_gmv:,.2f} "
    f"＋ 未归类（无 username）{unclassified_gmv:,.2f}。"
)
if order_col is not None:
    st.caption(recon + f" 人均出单基于列「{order_col}」计算。")
else:
    st.caption(
        recon + " ⚠️ 未在 Creator List 中找到出单数/订单数列，"
        "「人均出单」已省略。如需此指标，请告诉我对应的列名。"
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
