# -*- coding: utf-8 -*-
"""
NailVesta 國內達人組 — 交接 SOP 手冊
=====================================
給接手的人用的「照著做就會」操作手冊。
內容整理自兩份原始文件：
  - NailVesta_國內達人組日常任務（廣達組日常工作流程）
  - 深達工作（深達組日常／每週／每月工作）

只依賴 streamlit 一個套件，方便部署到 Streamlit Cloud。
若要新增/修改內容，直接改下方各 render_* 函式裡的字串即可。
"""

import os

import streamlit as st

# app.py 所在目錄，用來定位同層的圖片等資源
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))


def asset(name):
    return os.path.join(ASSET_DIR, name)


def first_existing(*names):
    """回傳第一個實際存在的檔案路徑（容忍底線/空格、副檔名差異）。"""
    for n in names:
        p = asset(n)
        if os.path.exists(p):
            return p
    return None

# =============================================================
# 頁面設定
# =============================================================
st.set_page_config(
    page_title="NailVesta 達人組交接 SOP",
    page_icon="💅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# 樣式
# =============================================================
st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; max-width: 1100px;}
      h1, h2, h3 {letter-spacing: .5px;}
      .tag {display:inline-block; padding:2px 10px; border-radius:12px;
            font-size:0.8rem; font-weight:600; margin-right:6px;}
      .tag-guang {background:#e0f2fe; color:#0369a1;}
      .tag-shen  {background:#f3e8ff; color:#7e22ce;}
      .card {border:1px solid #e5e7eb; border-radius:12px; padding:16px 18px;
             margin-bottom:14px; background:#ffffff;}
      .card h4 {margin:0 0 8px 0;}
      .muted {color:#6b7280; font-size:0.9rem;}
      .pill {display:inline-block; padding:2px 10px; border-radius:8px;
             font-weight:700; margin-right:6px;}
      .s   {background:#dcfce7; color:#15803d;}
      .ak  {background:#fef9c3; color:#a16207;}
      .bk  {background:#ffedd5; color:#c2410c;}
      .bs  {background:#fee2e2; color:#b91c1c;}
      .sp  {background:#e0e7ff; color:#4338ca;}
      .warn{background:#fef2f2; border-left:4px solid #ef4444; padding:10px 14px;
            border-radius:6px; margin:8px 0;}
      .ok  {background:#f0fdf4; border-left:4px solid #22c55e; padding:10px 14px;
            border-radius:6px; margin:8px 0;}
      .step {background:#f8fafc; border-left:4px solid #3b82f6; padding:10px 14px;
             border-radius:6px; margin:8px 0;}

      /* Follow Up 橫向時間軸 */
      .fu-wrap{overflow-x:auto; padding:8px 0 6px;}
      .fu-timeline{display:flex; position:relative; min-width:780px;}
      .fu-track{position:absolute; left:1.5%; right:1.5%; top:148px;
                height:2px; background:#dcd8cd;}
      .fu-col{flex:1; display:flex; flex-direction:column; align-items:center;}
      .fu-slot{height:130px; width:100%; display:flex; justify-content:center;
               position:relative; padding:0 10px; box-sizing:border-box;}
      .fu-slot.top{align-items:flex-end;}
      .fu-slot.bot{align-items:flex-start;}
      .fu-slot.top.filled::after{content:""; position:absolute; left:50%; bottom:0;
               width:2px; height:18px; background:#dcd8cd; transform:translateX(-50%);}
      .fu-slot.bot.filled::before{content:""; position:absolute; left:50%; top:0;
               width:2px; height:18px; background:#dcd8cd; transform:translateX(-50%);}
      .fu-card2{max-width:190px; text-align:center;}
      .fu-card2 .t{font-weight:700; color:#3f3a30; font-size:0.95rem;}
      .fu-card2 .when{display:inline-block; margin:5px 0 7px; padding:1px 10px;
               border-radius:10px; background:#efe9dc; color:#8a7a55;
               font-size:0.72rem; font-weight:600;}
      .fu-card2 .d{font-size:0.78rem; color:#6b7280; line-height:1.45;}
      .fu-dot{position:relative; z-index:1; width:38px; height:38px; border-radius:11px;
              background:#efece4; border:1px solid #ddd8cc; color:#6b6147;
              display:flex; align-items:center; justify-content:center; font-weight:700;}

      /* 週報「週出單達人」兩欄示意 */
      .wk-ex{margin:6px 0;}
      .wk-row{display:flex; flex-wrap:wrap; align-items:center; gap:8px;
              padding:10px 12px; border:1px solid #e5e7eb; border-radius:10px;
              margin-bottom:8px; background:#fff;}
      .wk-label{font-weight:700; color:#7e22ce; min-width:54px;}
      .wk-chip{padding:2px 10px; border-radius:10px; font-size:0.8rem; font-weight:600;}
      .wk-chip.post{background:#e0f2fe; color:#0369a1;}
      .wk-chip.sale{background:#dcfce7; color:#15803d;}
      .wk-arrow{color:#9ca3af; font-weight:700; letter-spacing:-1px;}
      .wk-counts{margin-left:auto; font-size:0.85rem; color:#374151;}

      /* 月報巢狀效益關係 */
      .nest-out{border:2px solid #cbd5e1; border-radius:12px; padding:14px;
                background:#f8fafc;}
      .nest-mid{border:2px solid #c4b5fd; border-radius:10px; padding:12px;
                background:#faf5ff; margin-top:10px;}
      .nest-in{border:2px dashed #a78bfa; border-radius:8px; padding:10px;
               background:#f3e8ff; margin-top:10px;}
      .nest-lab{font-weight:700; font-size:0.9rem;}
      .nest-sub{font-size:0.78rem; color:#6b7280; display:block; margin-top:2px;}

      /* 達人生命週期流程 */
      .flow{display:flex; flex-wrap:wrap; gap:8px; margin:8px 0;}
      .flow-node{flex:0 0 auto; width:150px; background:#fff; border:1px solid #e5e7eb;
                 border-left:4px solid #cbd5e1; border-radius:10px; padding:8px 10px;}
      .flow-node.g{border-left-color:#38bdf8;}
      .flow-node.s{border-left-color:#a78bfa;}
      .flow-node.n{border-left-color:#cbd5e1;}
      .flow-node .fn{display:inline-flex; width:20px; height:20px; border-radius:6px;
                     background:#f1f5f9; color:#475569; font-size:0.72rem; font-weight:700;
                     align-items:center; justify-content:center; margin-bottom:4px;}
      .flow-node .flab{font-weight:700; font-size:0.85rem; display:block; line-height:1.3;}
      .flow-node .fpg{font-size:0.72rem; color:#9ca3af;}
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================
# 側欄導覽
# =============================================================
st.sidebar.title("💅 NailVesta 達人組")
st.sidebar.caption("交接 SOP 手冊 · 照著做就會")

PAGES = [
    "🏠 交接須知（先看這頁）",
    "📖 名詞速查",
    "📅 每日工作時間表",
    "🟦 廣達組 SOP",
    "🟪 深達組 SOP",
    "⭐ 評級制度（3.0）",
    "💬 話術庫（複製即用）",
    "📦 包裹狀態與水單",
    "🔗 常用連結與系統",
]
page = st.sidebar.radio("選擇章節", PAGES, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<span class='tag tag-guang'>廣達</span> 新合作 / 尚未出單的達人<br>"
    "<span class='tag tag-shen'>深達</span> 長期 / 有出單 / 有轉化的達人",
    unsafe_allow_html=True,
)
st.sidebar.caption("有疑問先查這份手冊；查不到再問營銷部門 → 達人部門。")


# =============================================================
# 深達觸達話術（再合作邀約）
# =============================================================
SHEN_OUTREACH_T1 = """Hi love
It's Ava from NailVesta! I hope you've been doing amazing — I'd love to team up with you again. We just launched a bunch of new styles and I immediately thought of you
If you're up for another collab, you can pick 2–3 of your fave styles using this link so I can send them your way:
https://forms.gle/3jQ3ainsrEyqzXjJA
For this collab, we'd love to keep it simple:
• For each set you choose, please post at least 1 video per week
• Ideally, all 2–3 sets can be filmed in face-to-camera + voiceover + hands-on (application) style
This type of content performs really well — based on TikTok data, face-to-camera product reviews have around a 61% conversion rate
If you follow this format, I'll be able to prioritize your videos for ad boosting on our end to help maximize your exposure and results
Can't wait to create something cute together again!
With love,
Ava"""

SHEN_OUTREACH_T0 = """Hi love 💖
It's Ava from NailVesta! I hope you've been doing amazing — I'd love to team up with you again. We just launched a bunch of new styles and I immediately thought of you ✨
If you're up for another collab, you can pick 3–4 of your fave styles using this link so I can send them your way:
✨ https://forms.gle/ZRYf2D2KWETX3n2y7
For this collab, we'd love to set a simple structure:
• For each set you choose, please post at least 1 video per week
• Ideally, all 3–4 sets can be filmed in face-to-camera + voiceover + hands-on (application) style
This type of content performs really well — based on TikTok data, face-to-camera product reviews have around a 61% conversion rate 📈
If you follow this format, I'll be able to prioritize your videos for ad boosting on our end to help maximize your exposure and results 💅✨
Can't wait to create something cute together again!
With love,
Ava"""


# =============================================================
# Follow Up 話術（複製即用）
# 格式：(階段, 主旨 or None, 內文, 備註 or "")
# =============================================================
GUANG_FU = [
    ("1.0", None, """Hi love!! 💖 Welcome to the NailVesta fam!

Your sample is shipping today and should arrive within 5 business days

Inside your package, you'll also find a little pamphlet with filming tips + a Discord QR code — feel free to scan and join our creator community 💕

For best performance, we highly recommend a face-to-camera application + review video (this is the most important ✨) with:
• clear nail close-ups (first 3 seconds)
• bright/natural lighting
• sharing your real thoughts

Top-performing content (based on TikTok official conversion data):
▪️Product reviews (61%)
▪️"Worth it?" / honest opinions (44%)
▪️Before & after results (41%)

Content like this performs better and has a higher chance to be selected for paid ad boosting on our side ✨

Let's make magic together 💖""", ""),
    ("2.0", None, """Hey babe! 💕 Your NailVesta package is almost there! 📦

Don't forget — there's a Discord QR code inside the package, feel free to join and connect with other creators 💖

When posting, please:
• tag @nailvesta_official
• use #NailVesta
• add the product link

If your video includes face-to-camera + application (talking & showing on hand) + clear nail details + good lighting, we'll support it with paid ad boosting to help increase your exposure, views, followers, and conversions ✨

Top-performing content (based on TikTok official conversion data):
▪️Product reviews (61%)
▪️"Worth it?" / honest opinions (44%)
▪️Before & after results (41%)

Can't wait to see your content — so excited for this collab 💕""", ""),
    ("4.0", None, """Hi gorgeous! 💖 Just checking in to see how it's going with your NailVesta set! I am so excited to see your video. If you're able to post it this week, that would be amazing!

No worries if you've been busy, but if you need any help or have questions, just let me know. Thanks so much for being part of this collab! 💅""", ""),
    ("5.0", None, """Hi darling ✨ Just wanted to gently check in. So excited to see your video!

Each set is handmade with love and takes a few hours to create, so it truly means a lot to me 💖

If you have an idea of when you might post, would love to hear! No rush at all. Just here cheering you on. Let me know if I can help with anything!""", ""),
    ("6.0", None, """Hi pretty 💕 Just checking in! Totally understand how busy life gets. I really appreciate your time and effort!

If you're still planning to post, would you mind sharing a rough timeline? And if anything's changed, no worries at all. Just plz let me know so we can adjust 💖

Here if you need anything! 😊""", ""),
]

SHEN_FU = [
    ("1.0", "Your NailVesta package is arriving soon 💕", """Hi love 🤍

Just wanted to give you a quick update — your NailVesta package has officially been shipped out and should arrive within around 3–5 business days ✨

Here's your USPS tracking number so you can follow it on the way:

LV067303122U

I'm so excited for you to get it and can't wait to see what you create 💖

And just a little reminder, once you post your video, please send me your AD CODE too 🫶✨ I'd love to prioritize boosting your video on TikTok so it can get even more reach and conversions.

So excited for your content!

Best,
Ava""",
     "粗體部分：「has officially been shipped out」「around 3–5 business days」「追蹤碼」。"
     "追蹤碼 LV067303122U 是範例，每位達人不同，發送前記得換成實際碼。"),
    ("4.0", "NailVesta – Posting now could bring more reach & sales 💖", """Hi love! It's Ava. Just wanted to check in real quick, Hope you're doing well 💖
I was wondering if your package arrived safely! Also wanted to share that we've been seeing a nice boost in video reach lately, so it's a great time for content to get seen by more people
If you're planning to post soon, your video could definitely benefit from the extra exposure. And more views often lead to more sales too 💅 Let me know if you need anything or have any questions!""", ""),
    ("5.0", "Excited to See Your Video! ✨", """Hey love,
Just checking in again—we're really looking forward to seeing your NailVesta video! Your creativity always shines, and we know your audience will love it too. 💕
Just wanted to check in and see if you have an estimated post date. This will help us align our promotion schedule. If there's anything holding you back, we'd love to assist in any way we can. We appreciate your collaboration and can't wait to see your stunning content! 💅✨
Looking forward to hearing from you soon!""", ""),
    ("6.0", "Urgent: Final Follow-Up on Your NailVesta Video 💖", """Hey love,
We completely understand that life gets busy, and we truly appreciate your time and creativity! However, it's now been four weeks since you received your NailVesta set, and we haven't seen your video yet.
If you're still planning to post, please let us know your timeline ASAP, so we can schedule accordingly. If you're facing any challenges or need assistance, we're happy to help! However, if you're unable to proceed with the post, kindly let us know so we can adjust our plans accordingly.
We value our collaboration and your creative work, and we'd love to continue working with you! Please provide an update at your earliest convenience.
Looking forward to your response! 💖""", ""),
]


# =============================================================
# 3.0 影片反饋話術（依評級情境）
# 結構：{情境標籤: {"note":..., "scripts":[(子標題, 內文)], "samples":[...]}}
# =============================================================
GUANG_FEEDBACK = {
    "S — 優秀，完全符合": {
        "note": "動作：誇達人 + 要廣告碼 + 要聯繫方式。逐條評級後，在 Shop Chat 發送反饋 + 視頻示例。",
        "scripts": [
            ("沒出單（no sales yet）", """Hey Beautiful! Just saw your video, and wow, I'm absolutely in love with it! 😍 You seriously nailed the look! If you're open to it, could you share your preferred way of contact for long-term collab? 💖

By the way, if you post a few more videos, it really helps boost visibility and sales — the more content, the more exposure ✨

Also, could you send over your ad code when you get a chance? So we can promote your video."""),
            ("新視頻要 code（短版）", """Hey sweetie, INLOVE with your new video! Could you send me the ad code for it? 💗
（視頻連結）"""),
        ],
        "samples": ["絕好 S（僅供參考）：https://www.tiktok.com/@_savannahlee/video/7516642180362947871"],
    },
    "AK / AS / C — 優良，差一點到 S": {
        "note": "AK＝有口播的准 S；AS＝沒口播的准 S 或准 C（注意區分 C 和 AS）。發對應話術並要 Ad Code。沒有對應 Scenario 可歸類、單純觀感差時，用下方話術。",
        "scripts": [
            ("AK", """Hi babe 🥹💖 I just watched your video and it's sooo beautiful. If you are open to posting more, that would be amazing!

Also, when you get a chance, could you please share the ad code with me? That way I can boost it with a budget to help your video reach even more people"""),
            ("AS / C", """Hey love! I just watched your video and I'm obsessed! 😍 You did such an amazing job, seriously! 😭✨

If you're open to it, would you be down to post another video that feels a bit more like a personal review? Maybe sharing how the nails feel, what stood out to you, or why you'd recommend them — I'd be so excited to promote that one too! 💖

Also, could you send over your ad code when you get a chance? So we can promote your video."""),
        ],
        "samples": [
            "AK（多為觀感差的口播視頻）：https://www.tiktok.com/@redheadgirl01_/video/7542292427055418637",
            "AS（多為佩戴視頻）：https://www.tiktok.com/@strwbrryww/video/7541056938725969182",
        ],
    },
    "BK1 — 有口播，太長 >60s": {
        "note": "",
        "scripts": [("", """Hey babe! 💖 I just watched your video, and wow, it's absolutely stunning! 😍 I'm so impressed with how much effort you put into it!

One tiny tweak that could make it even more impactful is shortening it a little for ads. Reviews around 40 seconds tend to perform the best.

Would you be open to creating a shorter version? I'd be so excited to promote it and help it shine even brighter! ✨💕""")],
        "samples": ["多為視頻太長且拖沓：https://www.tiktok.com/@neida_velasquez/video/7496697819122765087"],
    },
    "BK2 — 有口播，產品拍攝不清晰": {
        "note": "光線暗 / close-up 沒聚焦 / 產品細節少。",
        "scripts": [("", """Hey love! I just watched your video, and OMG, I'm obsessed! 😍 You absolutely nailed it! 😭✨ It's nearly perfect!

I just have a small suggestion. Maybe include more close-ups of the nails and using brighter lighting can really showcase the details.

Would you be open to filming another version? I'd love to promote that one too!""")],
        "samples": [
            "https://www.tiktok.com/@urfavbpdlibra/video/7539363368088440095",
            "https://www.tiktok.com/@queenzeyrle/video/7545247441872866573",
        ],
    },
    "BK3 — 有口播，太短 <20s": {
        "note": "有口播但太倉促、賣點不夠。",
        "scripts": [("", """Hey love! I just watched your video, and oh my gosh, it's absolutely stunning!😍

The only thing is, if the video were a little longer, around 30-60 seconds, it could work even better for ads.

Would you be open to creating another video? I'd love to promote it. I just know it's going to shine even brighter!✨""")],
        "samples": ["https://www.tiktok.com/@_..ornelas.._/video/7538128187088293134"],
    },
    "BK4 — 有口播，沒上手": {
        "note": "多為沒上手、觀感不美的視頻。",
        "scripts": [("", """Hi love! Your video is awesome — we really appreciate the voiceover! 💖

If you have time, would you be open to filming another video wearing the nails? We'd love to showcase the full effect!""")],
        "samples": ["https://www.tiktok.com/@sheinahdiah/video/7545955089463119135"],
    },
    "Haul — 混合多產品開箱": {
        "note": "",
        "scripts": [("", """Hey love! 💖 I just saw your video, and I'm obsessed witch your style! ✨

Would you be open to filming a video that highlights just our nails?

I totally get that you have multiple promos, but a dedicated video would mean so much to us! I really appreciate it! ❤️""")],
        "samples": ["https://www.tiktok.com/@kaysk4ta/video/7545149495529524494"],
    },
    "BS1 — 無口播，沒上手": {
        "note": "",
        "scripts": [("", """Hi love! Your video is absolutely gorgeous — thank you so much for putting it together 💖
If you have a little extra time, would you be open to filming another one actually wearing the nails on your hands? It would be amazing to show how they look when worn, how they feel, and maybe even share what stood out to you or why you'd recommend them 💅✨

I'd be so excited to promote that version too! 💖 Can't wait to hear what you think!""")],
        "samples": ["https://www.tiktok.com/@avery.dryman/video/7545949400527359246"],
    },
    "BS2 — 無口播，沒賣點": {
        "note": "一般視頻時長短。",
        "scripts": [("", """Hey love! I just watched your video and I'm obsessed! 😍 You did such an amazing job, seriously!

If you're open to it, would you be open to posting another video that feels a bit more like a personal review? Maybe sharing how the nails feel, what stood out to you, or why you'd recommend them.

I'd be so excited to promote that one too! 💖 Let me know what you think!""")],
        "samples": ["https://www.tiktok.com/@msfazo/video/7545528516960357663"],
    },
    "D — 刪視頻 / 還沒發片": {
        "note": "讓達人重發。",
        "scripts": [("", """Hey love! I was looking for your videos, but could not find any on your page. Could you please post a video? Each set takes 2 hours to make and costs a lot to ship. I really need your help in promoting them. Can you help me out? 🥺🫶Thank youuu!💖""")],
        "samples": [],
    },
    "T — 特殊：鏈接 / 指甲對不上": {
        "note": "",
        "scripts": [
            ("我們的指甲、別人的鏈接", """Hi love! 💖 Thank you so much for sharing the video, it looks amazing! We just noticed the product link goes to another nail brand, so we wanted to kindly check in and see if that was a mix-up. Totally understand if it was unintentional. I just wanted to make sure your audience could find the right nails! 💅✨ Let us know if you need the correct link!"""),
            ("別人的指甲、我們的鏈接（若已發過 3.0 就不用發這段）", """Hi love! 💖 Thank you so much for sharing your video, it looks great! We just noticed that the video features another brand's nails, but it's linked to us. Just wanted to kindly check in, in case there was a mix-up! 💅

Totally understand if it was unintentional, these things happen! If you're open to it, would you be willing to film another video showcasing our set? We'd absolutely love to see you wear and highlight our design, and we're happy to resend any info you need. Let us know how we can help! ✨"""),
        ],
        "samples": [],
    },
}

# B 類（BK/BS/Haul）追碼話術
GUANG_B_ADCODE_PENDING = """Also, can I have your ad code so i can promote your videos through Spark ads? thanks!!!

when you generate the ad code, could you please set the ad code's lifespan to the 365 days? this will help us drive more traffic to your videos! ❤️"""

GUANG_B_ADCODE_DONE = """I'll pass your ad code to my colleague and include your video in our advertising plan 🫶"""


SHEN_FEEDBACK = {
    "要碼（主旨：Quick Request 💗 May I Have Your Ad Code?）": {
        "note": "",
        "scripts": [("", """Hi babe 🥹💖 I just watched your video and it's sooo beautiful. If you are open to posting more, that would be amazing!

Also, when you get a chance, could you please share the ad code with me? That way I can boost it with a budget to help your video reach even more people""")],
        "samples": [],
    },
    "S（主旨：Quick idea to boost your NailVesta video 💖）": {
        "note": "",
        "scripts": [("", """Hey beautiful! 💖 I just saw your video and I'm honestly in love 😍 you absolutely nailed the look!

Also, posting a few more videos really helps boost visibility and sales, your content has so much potential 💕

And when you get a chance, could you send over your ad code? I'd love to support your video with ads 💖""")],
        "samples": [],
    },
    "AK": {
        "note": "",
        "scripts": [("", """Hi babe 🥹💖 I just watched your video and it's sooo beautiful — you did such an amazing job!

If you're open to posting more, that would be incredible, I'd love to see more of your content ✨

Also, when you get a chance, could you share your ad code with me? I'd love to support it with budget and help your video reach even more people 💕""")],
        "samples": [],
    },
    "AS / C": {
        "note": "",
        "scripts": [("", """Hey love! I just watched your video and I'm obsessed! 😍 You did such an amazing job, seriously! 😭✨

If you're open to it, would you be down to post another video that feels a bit more like a personal review? Maybe sharing how the nails feel, what stood out to you, or why you'd recommend them — I'd be so excited to promote that one too! 💖

Also, could you send over your ad code when you get a chance? So we can promote your video.""")],
        "samples": [],
    },
    "BK1": {
        "note": "",
        "scripts": [("", """Hey babe! 💖 I just watched your video, and wow, it's absolutely stunning! 😍 I'm so impressed with how much effort you put into it!

One tiny tweak that could make it even more impactful is shortening it a little for ads. Reviews around 40 seconds tend to perform the best.

Would you be open to creating a shorter version? I'd be so excited to promote it and help it shine even brighter! ✨💕""")],
        "samples": [],
    },
    "BK2": {
        "note": "",
        "scripts": [("", """Hey love! 💖 I just watched your video and I'm obsessed 😍 you absolutely nailed it — it's sooo close to perfect!

Just a small suggestion — adding a few more close-ups of the nails and using slightly brighter lighting could really make the details pop even more ✨

Would you be open to filming another version? I'd LOVE to promote that one too 💕""")],
        "samples": [],
    },
    "BK3": {
        "note": "",
        "scripts": [("", """Hey love! 💖 I just watched your video and it's absolutely stunning 😍 you did such an amazing job!

I feel like if it were just a little longer — around 30–60 seconds — it could perform even better for ads ✨

Would you be open to creating another version? I'd LOVE to promote it and help it reach even more people 💕""")],
        "samples": [],
    },
    "BK4": {
        "note": "",
        "scripts": [("", """Hey love! 💖 I just watched your video and it looks amazing — we really appreciate the voiceover, you did such a great job 😍

If you have time, would you be open to filming another version actually wearing the nails?

I think showing the full look on your hands would make it even more impactful, and I'd LOVE to promote that one too ✨""")],
        "samples": [],
    },
    "Haul": {
        "note": "",
        "scripts": [("", """Hey love! 💖 I just saw your video and I'm obsessed with your style 😍

Would you be open to filming a version that highlights just our nails? I think a dedicated video would really let the details shine ✨

Totally understand you have multiple promos — we really appreciate it, and it would mean so much to us 💕""")],
        "samples": [],
    },
    "BS1": {
        "note": "",
        "scripts": [("", """Hi love! 💖 I just watched your video and it's absolutely gorgeous — thank you so much for putting it together 😍

If you have a little extra time, would you be open to filming another version actually wearing the nails on your hands? I think showing how they look when worn, how they feel, and what stood out to you would make it even more impactful ✨

I'd LOVE to promote that version too 💕 can't wait to hear what you think!""")],
        "samples": [],
    },
    "BS2": {
        "note": "",
        "scripts": [("", """Hey love! 💖 I just watched your video and I'm obsessed 😍 you did such an amazing job!

If you're open to it, would you be down to post another version that feels more like a personal review? Maybe sharing how the nails feel, what stood out to you, or why you'd recommend them ✨

I'd LOVE to promote that one too 💕 let me know what you think!""")],
        "samples": [],
    },
}


# =============================================================
# 各章節
# =============================================================
FU_STEPS = [
    ("Follow Up 1.0", "當天", "樣品寄出當日：歡迎加入、說明品牌理念，預告 5 個工作天內送達"),
    ("Follow Up 2.0", "發貨後兩天", "包裹即將送達：提醒查看拍攝指南，說明廣告預算支援（$20k+）"),
    ("Follow Up 3.0", "發布視頻完成", "評級視頻並回反饋給達人，請他做修改及更正"),
    ("Follow Up 4.0", "未發片過 2 週", "溫和催促：詢問進度、表達期待、提供協助"),
    ("Follow Up 5.0", "未發片過 3 週", "跟進催促：詢問是否需要幫忙，或有什麼個人因素"),
    ("Follow Up 6.0", "未發片過 4 週", "最後提醒：強調手工製作的用心，請求時間表或狀態更新"),
]


def build_fu_timeline():
    cols = []
    for idx, (title, when, desc) in enumerate(FU_STEPS, start=1):
        card = (
            f"<div class='fu-card2'><div class='t'>{title}</div>"
            f"<div class='when'>{when}</div><div class='d'>{desc}</div></div>"
        )
        if idx % 2 == 1:  # 奇數放上方
            top = f"<div class='fu-slot top filled'>{card}</div>"
            bot = "<div class='fu-slot bot'></div>"
        else:              # 偶數放下方
            top = "<div class='fu-slot top'></div>"
            bot = f"<div class='fu-slot bot filled'>{card}</div>"
        cols.append(f"<div class='fu-col'>{top}<div class='fu-dot'>{idx}</div>{bot}</div>")
    return (
        "<div class='fu-wrap'><div class='fu-timeline'>"
        "<div class='fu-track'></div>" + "".join(cols) + "</div></div>"
    )


def render_feedback_section(feedback, key_prefix):
    """3.0 影片反饋：選評級 → 顯示對應話術 + 參考影片。"""
    choice = st.selectbox(
        "選擇評級／情境，看對應反饋話術",
        list(feedback.keys()),
        key=f"{key_prefix}_fb",
    )
    item = feedback[choice]
    if item.get("note"):
        st.markdown(f"<div class='ok'>{item['note']}</div>", unsafe_allow_html=True)
    for sub, text in item["scripts"]:
        if sub:
            st.markdown(f"**{sub}**")
        st.code(text, language=None)
    if item.get("samples"):
        st.markdown("**參考影片**")
        st.markdown("\n".join(f"- {s}" for s in item["samples"]))


# 達人生命週期：(編號, 名稱, 類別 g/s/n, 對應分頁)
LIFECYCLE = [
    ("1", "達人申請", "g", "廣達·上午"),
    ("2", "批達人", "g", "廣達·上午"),
    ("3", "寄樣 1.0／2.0", "g", "廣達·Follow Up"),
    ("4", "達人發片", "n", ""),
    ("5", "評級 3.0", "g", "廣達·下午"),
    ("6", "反饋＋要碼", "n", "話術／評級制度"),
    ("7", "廣告投放", "n", "Spark ad"),
    ("8", "出單", "n", ""),
    ("9", "標記可深達", "g", "PC"),
    ("10", "觸達轉深達", "s", "深達·觸達流程"),
    ("11", "深達維護", "s", "深達·Follow Up／月報"),
]


def build_lifecycle():
    nodes = []
    for num, label, cls, pg in LIFECYCLE:
        pgline = f"<span class='fpg'>{pg}</span>" if pg else ""
        nodes.append(
            f"<div class='flow-node {cls}'><span class='fn'>{num}</span>"
            f"<span class='flab'>{label}</span>{pgline}</div>"
        )
    return "<div class='flow'>" + "".join(nodes) + "</div>"


# 名詞速查：(名詞, 說明)
GLOSSARY = [
    ("廣達", "廣度達人：新合作 / 尚未出單的達人，多靠平台合作、有時效性發片。"),
    ("深達", "深度達人：長期 / 已出單 / 有轉化的達人，由公司發貨、發片無時效壓力。"),
    ("S 級", "最高影片評級：完全符合推廣要求。動作＝誇達人＋要廣告碼＋要聯繫方式。"),
    ("AK / AS / C", "準 S 評級。AK＝有口播沒露臉；AS＝沒口播有露臉；C＝高級美甲展示。"),
    ("BK1–BK4", "有口播但有問題（太長 / 拍不清 / 太短 / 沒上手），回覆優先級 BK4>BK3>BK2>BK1。"),
    ("BS1 / BS2", "無口播：BS1 沒上手、BS2 沒賣點。"),
    ("T / Haul / D", "特殊：T＝鏈接或指甲對不上 / 西語；Haul＝混多產品；D＝刪片，要重發。"),
    ("PC（可深達）", "達標的廣達可標記為「可深達」，後續轉入深達流程。"),
    ("觸達", "把表現好的廣達轉成深達（深達二次合作）的動作。"),
    ("T0 / T1 / T2S", "達人分層：T0＝28 單以上；T1＝10–28 單；T2S＝新 / 潛力達人。"),
    ("Follow Up 1.0–6.0", "寄樣後到催發片的分階段跟進話術。"),
    ("3.0 反饋", "影片發布後，依評級回給達人的反饋話術。"),
    ("水單", "補寄出貨單。深達補寄分類為「深度達人單」。"),
    ("甲冊", "寄給達人的美甲樣本冊；有甲冊發片轉化率特別好。"),
    ("ad code / 廣告碼", "達人授權影片可被投放廣告的代碼；建議設 365 天效期。"),
    ("Spark ad", "用達人原生影片去投放的廣告形式。"),
    ("均播", "平均播放量。批達人參考門檻之一（500+）。"),
    ("GMV", "商品交易總額（成交金額）。"),
    ("AOV", "平均訂單金額（客單價）。"),
    ("ASP", "平均售價。"),
    ("Items Sold", "售出件數。"),
    ("達人 ROI", "本 SOP 定義：出單數量 ÷ approve 達人數 × 100%。"),
    ("flat fee", "付費合作（固定費用），深達月預算 2000。"),
    ("KOL", "關鍵意見領袖（較具影響力的合作達人）。"),
    ("Lark", "批達人、評級時的主要操作後台（含 Affiliate List / Account）。"),
    ("curva", "廣達廣告表 approve 用的工具（深達每日工作）。"),
    ("fastmoos", "分析達人 GMV、均播、品類的工具（深達建聯篩選用）。"),
    ("CU / CR 消息", "每日要回覆的訊息類別；CU 回覆情境見營銷部門 → 達人部門文件。"),
]


def render_glossary():
    st.title("📖 名詞速查")
    st.caption("看其他頁遇到不懂的詞，回這頁查。定義以本 SOP 與團隊內部說法為準。")
    rows = "\n".join(f"| **{t}** | {d} |" for t, d in GLOSSARY)
    st.markdown("| 名詞 | 說明 |\n|---|---|\n" + rows)


def render_intro():
    st.title("🏠 交接須知")
    st.markdown(
        "歡迎接手 NailVesta 國內達人組。這份手冊把日常工作拆成可照做的步驟，"
        "**遇到不確定的，先回來查對應章節**。"
    )

    st.subheader("這個團隊在做什麼")
    st.markdown(
        "我們透過 TikTok 達人合作推廣 NailVesta 的美甲產品，分成兩條線："
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "<div class='card'><h4>🟦 廣達（廣度達人）</h4>"
            "<ul>"
            "<li>新合作達人</li>"
            "<li>尚未出單的達人</li>"
            "<li>主要靠平台合作、有時效性發片</li>"
            "</ul>"
            "<span class='muted'>日常：批達人、評級反饋、回私訊、優化達人池</span></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            "<div class='card'><h4>🟪 深達（深度達人）</h4>"
            "<ul>"
            "<li>長期合作達人</li>"
            "<li>已出單、有轉化率的達人</li>"
            "<li>透過公司發貨，不跟平台合作，發片無時效壓力</li>"
            "</ul>"
            "<span class='muted'>日常：維護關係、建聯、盯數據、寄甲冊、做報表</span></div>",
            unsafe_allow_html=True,
        )

    st.subheader("每天最重要的三件事")
    st.markdown(
        "<div class='step'>1. <b>批達人</b>：上午審批當日達人申請，<b>24 小時內</b>完成所有待審。</div>"
        "<div class='step'>2. <b>評級 + 反饋</b>：把前一天發布的影片評級（3.0 系統），並回覆達人。</div>"
        "<div class='step'>3. <b>回私訊</b>：CU / CR、Email、Discord、Instagram 的訊息要及時回。</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='ok'>🌅 工作以<b>洛杉磯時間下午</b>為主（對應北京上午）。完整時段見「每日工作時間表」。</div>",
        unsafe_allow_html=True,
    )

    st.subheader("達人生命週期（先看懂全貌）")
    st.markdown("一個達人從申請到變成長期深達，會走過這些階段。每格標了對應分頁：")
    st.markdown(build_lifecycle(), unsafe_allow_html=True)
    st.markdown(
        "<span class='tag tag-guang'>廣達</span> 藍色階段　"
        "<span class='tag tag-shen'>深達</span> 紫色階段　"
        "<span class='muted'>灰色為共用流程</span>",
        unsafe_allow_html=True,
    )

    st.subheader("第一週這樣上手")
    st.markdown(
        "<div class='step'><b>第 1–2 天</b>：讀「交接須知」「名詞速查」「達人生命週期」，"
        "跟上一手要齊：各系統網址（Canva）、Lark／廣告表／總表權限、群組與 Discord。</div>"
        "<div class='step'><b>第 3–4 天</b>：跟著做「廣達·上午批達人」與「廣達·下午評級 3.0」，"
        "邊做邊查「評級制度」與話術。</div>"
        "<div class='step'><b>第 5–7 天</b>：熟悉私訊回覆與 Follow Up，了解「深達觸達流程」與"
        "「表單回覆→下單」，知道何時把廣達轉深達。</div>"
        "<div class='step'><b>第二週起</b>：接手週報，月底跟著做月報（可用 AI 幫忙算）。</div>",
        unsafe_allow_html=True,
    )


def render_schedule():
    st.title("📅 每日工作時間表")
    st.caption("每日固定節奏，評級與日報採「順序制」由組員輪值。週日加做達人週報。")

    st.markdown(
        """
| 洛杉磯時間 | 北京時間 | 工作內容 |
|---|---|---|
| 4PM–6PM | 7AM–9AM | **視頻評級 3.0 反饋**（評前一天發布的影片並回反饋） |
| 6PM–9PM | 9AM–12PM | **回覆 CU、CR 消息** ＋ **批達人** |
| 9PM–10PM | 12PM–1PM | 午休 |
| 10PM–11PM | 1PM–2PM | **達人池優化**：搜尋新潛力達人、標記高品質素材 |
| 11PM–1AM | 2PM–4PM | **達人日報**（順序制）；週日加做**達人週報** |
"""
    )
    st.markdown(
        "<div class='ok'>「順序制／輪值」：評級反饋與日報由組員依排班表輪流負責，"
        "交接時記得跟上一手確認本週輪到誰。</div>",
        unsafe_allow_html=True,
    )

    st.subheader("✅ 今日工作清單")
    st.caption("邊做邊勾。勾選只在本次瀏覽有效，重新整理會清空，每天重新勾。")
    daily_tasks = [
        "視頻評級 3.0 並回反饋（前一天發布的影片）",
        "回覆 CU、CR 消息",
        "批達人（當日申請，24 小時內完成）",
        "達人池優化：搜尋新潛力達人、標記高品質素材",
        "達人日報（輪值）",
        "（週日）達人週報",
    ]
    done = 0
    for i, t in enumerate(daily_tasks):
        if st.checkbox(t, key=f"daily_{i}"):
            done += 1
    st.progress(done / len(daily_tasks), text=f"已完成 {done}/{len(daily_tasks)}")


def render_guang():
    st.title("🟦 廣達組 SOP")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["☀️ 上午：批達人", "🌙 下午：評級與反饋",
         "🤝 達人邀約 & Follow Up", "📊 週報製作"]
    )

    # ---- 上午：批達人 ----
    with tab1:
        st.subheader("核心任務")
        st.markdown(
            "每日上午審批達人申請，**確保 24 小時內完成所有待審項目**。"
            "透過 Lark 篩選當日合作申請，核對達人資料與庫存。"
        )

        st.subheader("操作步驟")
        st.markdown(
            "<div class='step'>1. 進入 <b>Lark → AFFILIATE LIST</b> → 篩選 <b>合作日期 = 今天</b></div>"
            "<div class='step'>2. 逐筆輸入：<b>Handle、Status、Follower、款式、Size、佣金、Affiliate Link、TikTok Link</b></div>"
            "<div class='step'>3. <b>對庫存表</b>：該款式庫存 <b>少於 10 件不可發</b>，需私訊達人改款式（見話術庫「達人想換款式」）</div>"
            "<div class='step'>4. 確認 Follower 條件（見下）</div>"
            "<div class='step'>5. 特殊情況：達人 <b>GMV 很高、觀感好</b>，即使條件略差也可以批</div>",
            unsafe_allow_html=True,
        )

        st.subheader("✅ Follower 通過條件")
        st.markdown(
            "<div class='ok'>"
            "• 年齡 <b>18–34 歲佔比 > 25%</b><br>"
            "• <b>女性比例 > 50%</b><br>"
            "• <b>均播 500+</b>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.subheader("⛔ 不批的達人")
        st.markdown(
            "<div class='warn'>"
            "• 申樣 <b>2 次以上</b>未發片（可能是騙樣達人）<br>"
            "• Status 為 <b>6.0</b><br>"
            "• 內容評級<b>連續 2 次以上低於</b> S / AK / AS / C（拍不出好視頻）<br>"
            "• Status 還是 <b>1.0 或 2.0</b> → 先不批<br>"
            "• 距上次合作 <b>需間隔 2 週以上</b>才可再批<br>"
            "• <b>西語達人基本不批</b>，除非 GMV 和均播特別高"
            "</div>",
            unsafe_allow_html=True,
        )

        st.subheader("⚠️ 特殊：深達在廣達裡申樣怎麼辦")
        st.markdown(
            "<div class='card'>"
            "1. 把該達人**入「深達表」，不入廣達表**<br>"
            "2. 深度合作 <b>status 改成「廣達發出」</b>，一樣填寫款式名稱、合作日期<br>"
            "3. 在群組以**接龍形式**寫：<code>handle - 廣達發出</code>"
            "</div>",
            unsafe_allow_html=True,
        )

    # ---- 下午：評級與反饋 ----
    with tab2:
        st.subheader("評級系統與影片反饋（4 步驟）")
        st.markdown(
            "<div class='step'><b>① 進入評級系統</b><br>"
            "從 Affiliate account 選擇時間排序 → 在 Lark 篩選 <b>發布日期 = 昨天</b> 的影片。</div>"
            "<div class='step'><b>② 處理「找不到人名」</b><br>"
            "去「找不到人名搜」頁面。若金額為 0 仍找不到 → 可能是<b>改名了</b>："
            "回溯合作日期查當時下的款式，再到 Affiliate 對名字。</div>"
            "<div class='step'><b>③ 視頻反饋</b><br>"
            "篩選 <b>Status ≠ 3.0</b> → 到私訊網頁，找對應話術回覆達人。</div>"
            "<div class='step'><b>④ 廣告素材處理</b><br>"
            "篩選「內容反饋」包含 <b>S、C、AK、AS</b> → 全選 Handle → 去廣告部門 → 廣告素材 → "
            "往下到底 → <b>只看前一天日期</b>（不是前一天的就刪掉）。<br>"
            "・<b>有碼</b> → 選「代投放」　・<b>沒碼</b> → 選「追蹤中」</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='ok'>評級完<b>一定要回反饋</b>給達人。各等級對應的判斷標準與要做的動作，見「評級制度（3.0）」章節。</div>",
            unsafe_allow_html=True,
        )

    # ---- 達人邀約 & Follow Up ----
    with tab3:
        st.subheader("達人邀約分層")
        st.markdown(
            "<div class='card'><h4>⭐ 達人邀約 1（T2S）— 新／潛力達人</h4>"
            "強調達人的真實性與潛力，提供 <b>15% 提升佣金、付費影片支援、創意指導</b>等完整資源。</div>"
            "<div class='card'><h4>⭐⭐ 達人邀約 2（T1）— 10–28 單</h4>"
            "針對偶爾出單的達人，提供 <b>2–3 個款式選擇</b>，強調新品上市與再次合作；語調溫暖親切，表達對其內容的欣賞。</div>"
            "<div class='card'><h4>⭐⭐⭐ 達人邀約 3（T0）— 28 單以上</h4>"
            "頂級達人可選 <b>3–4 個款式</b>，提供更多彈性與優先權；強調品牌對其的重視與共同成長的願景。</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Follow Up 時間軸")
        st.markdown(build_fu_timeline(), unsafe_allow_html=True)
        st.caption("奇數階段在上、偶數階段在下；畫面較窄時可左右滑動。")

        st.subheader("Follow Up 話術（複製即用）")
        st.caption("廣達以私訊發送。下方 1.0／2.0／4.0／5.0／6.0 為各階段話術；3.0（影片反饋）依評級選用，見下方。")
        for stage, _subj, body, note in GUANG_FU:
            st.markdown(f"**Follow Up {stage}**")
            st.code(body, language=None)
            if note:
                st.caption(note)

        st.markdown("---")
        st.subheader("Follow Up 3.0 — 影片反饋話術（依評級）")
        st.caption("逐條評級後，到 Shop Chat 發送反饋 + 視頻示例。")
        with st.expander("📎 B 類（BK / BS / Haul）共通規則 & 追碼話術"):
            st.markdown(
                "- 符合**深度合作標準**的 B 類達人，也要正常發反饋\n"
                "- 符合**廣告標準**的 B 類達人，發完 B 類話術後，加一句追碼話術 + 要聯繫方式\n"
                "- **普通** B 類達人，不主動要廣告碼\n"
                "- BK 評級／回覆**優先級為倒序**：BK4 > BK3 > BK2 > BK1"
            )
            st.markdown("**還沒發廣告碼**（先發「Ad Code 找碼圖解」——圖解在「💬 話術庫」頁——再附這段）：")
            st.code(GUANG_B_ADCODE_PENDING, language=None)
            st.markdown("**已發廣告碼**：")
            st.code(GUANG_B_ADCODE_DONE, language=None)
        render_feedback_section(GUANG_FEEDBACK, "guang")
        st.caption("同一份反饋話術，也可在「⭐ 評級制度（3.0）」頁找到（標廣達）。")

    # ---- 週報製作 ----
    with tab4:
        st.subheader("週報範圍")
        st.markdown(
            "統計區間：**上週五 → 這週四**。資料**每週五截圖**整理。"
        )

        st.markdown("**一、數據來源**")
        st.markdown(
            "<div class='step'>• <b>Affiliate Center > Analytics > Creator</b>："
            "拉 <b>7 天</b>，每週五截圖</div>"
            "<div class='step'>• <b>窗口期出單視頻數量</b>："
            "Analytics > All videos > <b>Video post date</b> 拉 7 天</div>",
            unsafe_allow_html=True,
        )

        st.markdown("**二、需要詢問皮總的項目**")
        st.markdown(
            "<div class='warn'>以下兩項要<b>問皮總</b>取得：<br>"
            "• <b>approve 數量</b>（上週五到這週四）<br>"
            "• <b>影片日均</b></div>",
            unsafe_allow_html=True,
        )

        st.markdown("**三、數據項目**")
        st.markdown(
            """
| 項目 | 怎麼算 / 在哪看 |
|---|---|
| **出單數量** | item sold（最上面有個總數） |
| **出單達人數** | 點到 0 為止，往前數看出幾單 |
| **達人 ROI** | 出單數量 ÷ approve 達人數 × 100% |
| **出單達人佔比** | 出單達人數 ÷ approve 達人數 × 100% |
"""
        )
        st.markdown(
            "<div class='step'><b>好影片數量</b>：在廣告表篩<br>"
            "・「發布日期 <b>晚於 -1</b>」<br>"
            "・「發布日期 <b>早於 +1</b>」<br>"
            "→ 兩者加起來的總數</div>",
            unsafe_allow_html=True,
        )

        st.markdown("**四、頭部達人數據**")
        st.markdown(
            "<div class='step'>• <b>影片數量</b>：view details →（取<b>前 10 名</b>）</div>"
            "<div class='step'>• <b>出單影片數量</b>：看 affiliate items sold <b>數字不為 0</b>，"
            "看有幾條影片</div>",
            unsafe_allow_html=True,
        )

        st.markdown("**五、頭部影片分析**")
        st.markdown(
            "<div class='step'>進 <b>Seller Center</b> → 按 <b>GMV 排序</b>（放<b>前 10 名</b>）</div>",
            unsafe_allow_html=True,
        )

        st.markdown("**六、CTR metrics**")
        st.markdown(
            "<div class='step'>記得<b>打勾 CTR</b></div>",
            unsafe_allow_html=True,
        )


def render_shen():
    st.title("🟪 深達組 SOP")
    st.caption("深達 = 長期、已出單、有轉化的達人。重點在「維護關係」與「找對人深化合作」。")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📆 每日工作", "🗓️ 每週工作", "📊 每月工作",
         "🎯 觸達流程（廣達轉深達）", "📝 表單回覆 → 下單", "📨 Follow Up 話術"]
    )

    with tab1:
        st.markdown(
            "<div class='step'><b>① 更改廣達廣告表狀態</b><br>"
            "透過 <b>curva</b> 點 approve，統計前一天有多少達人並回報中後台；"
            "同時檢查哪些達人好、哪些不好要過篩掉。<b>approve 時務必核對款式對不對。</b></div>"

            "<div class='step'><b>② 回覆 Email / Discord / Instagram</b><br>"
            "・<b>Email</b>：回覆合作內容；深達給 ad code 後入「深度達人 list」即可；與達人建聯。<br>"
            "・<b>Discord</b>：部分深達在裡面聯繫，用來維護達人。<br>"
            "・<b>Instagram</b>：達人會來找合作或聯繫舊深達（偏好 ins）。"
            "有些達人的 Email 是經紀人在回、可能要收費，<b>改用 ins 建聯有時可免付費合作</b>。</div>"

            "<div class='step'><b>③ 轉消息給 Sisley</b><br>黑白頭像的都需要轉。</div>"

            "<div class='step'><b>④ flat fee（付費合作）達人建聯</b><br>"
            "篩選優質付費合作達人，<b>月預算 2000</b>。主要看是否符合粉絲畫像、GMV、均播、帶的品類，"
            "再進一步談合作。可用 <b>fastmoos</b> 分析。</div>"

            "<div class='step'><b>⑤ 盯後台數據</b><br>"
            "看達人近期表現；找出<b>「廣達已出單但尚未轉深達」</b>的達人；"
            "可做一份分析報告，讓組員看怎麼找達人最好。</div>"

            "<div class='step'><b>⑥ 觀察深達發片狀況</b></div>"

            "<div class='step'><b>⑦ 看廣達日報</b><br>從日報分析中找出當日問題在哪、找出優化點。</div>"

            "<div class='step'><b>⑧ 評估寄甲冊</b><br>"
            "看哪些深達可以寄甲冊；<b>有甲冊去發布視頻，轉化率會特別好</b>。</div>"

            "<div class='step'><b>⑨ Approve Shopify 達人</b><br>"
            "到 Shopify 後台審批 affiliate 達人申請。<br>"
            "<a href='https://admin.shopify.com/store/wkb1va-ze/apps/affliate-by-secomapp/admin/affiliates?page=1&page_size=10' "
            "target='_blank'>開啟 Shopify Affiliates 後台 ↗</a></div>",
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown("### ① 達人週報製作")
        st.markdown("從深達表拉篩選製作週報並分析。以下是各統計項目的口徑與操作方式。")

        st.markdown(
            "<div class='warn'>⏱️ <b>影片類型統計一律採用「兩週前」的資料區間</b>，不是當週。</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='step'><b>影片類型與數量</b><br>"
            "在深達表選「<b>觸達</b>」這張表 → 開<b>篩選</b> → 統計各視頻類型及數量"
            "（採<b>兩週前</b>區間）。</div>"
            "<div class='step'><b>觸達族群</b><br>一樣到「<b>觸達</b>」表，用<b>篩選</b>統計。</div>"
            "<div class='step'><b>合作達人</b><br>用篩選看共有<b>多少位達人</b>。</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### 週出單視頻的達人（分兩欄，務必分清楚）")
        st.markdown(
            "<div class='card'>"
            "• <b>欄位 A — 週出單（不限發布週）</b>：該週<b>有出單</b>的達人，"
            "<b>不管影片是哪一週發的</b>。<br>"
            "• <b>欄位 B — 週出單 ＋ 當週發布</b>：該週有出單，"
            "<b>且影片也在同一週發布</b>的達人。"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class='wk-ex'>
  <div class='wk-row'>
    <span class='wk-label'>達人 A</span>
    <span class='wk-chip post'>影片發布 4/3</span>
    <span class='wk-arrow'>──→</span>
    <span class='wk-chip sale'>出單 5/20（報告週）</span>
    <span class='wk-counts'>計入 <b>欄位 A</b></span>
  </div>
  <div class='wk-row'>
    <span class='wk-label'>達人 B</span>
    <span class='wk-chip post'>影片發布 5/19（報告週）</span>
    <span class='wk-arrow'>──→</span>
    <span class='wk-chip sale'>出單 5/20（報告週）</span>
    <span class='wk-counts'>計入 <b>欄位 A ＋ 欄位 B</b></span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='ok'>記法：<b>欄位 B 是欄位 A 的子集</b>——只要當週出單就進 A；"
            "若影片又剛好在當週發，才同時進 B。達人 A 的影片是 4/3 發的，所以只進 A、不進 B。</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            "<div class='step'><b>② 優化話術</b><br>制定更好的廣達及深達話術，讓視頻效應最大化，"
            "讓發布的影片<b>S 級多一些</b>。</div>"
            "<div class='step'><b>③ 監督表現</b><br>同時監督深達與廣達的表現。</div>"
            "<div class='step'><b>④ 深達 Bonus</b><br>"
            "隨時看哪些深達達到<b>近 28 天出 10 單</b>，給他們發對應的 bonus。</div>"
            "<div class='step'><b>⑤ 新款寄送</b><br>新款給固定寄款的達人寄出。</div>",
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown("### 製作深達月報並分析")
        st.markdown("月報重點在「**算出深達帶來多少效益**」，再聚焦 Top 10 深達的貢獻。資料拉<b>整月</b>區間彙總。", unsafe_allow_html=True)

        st.markdown(
            "<div class='step'><b>① 月度深達整體效益</b><br>"
            "統計整月的 <b>GMV</b> 與 <b>Items Sold</b>——這就是<b>深達帶來的效益</b>。</div>"
            "<div class='step'><b>② 找出 Top 10 深達</b><br>"
            "從深達中排出當月<b>前 10 名</b>。</div>"
            "<div class='step'><b>③ 分析 Top 10 的貢獻</b><br>"
            "進一步算這 Top 10：<br>"
            "・給<b>深達整體</b>帶來多少效益（占深達 GMV／Items 的比例）<br>"
            "・給<b>店舖（整店）</b>帶來多少效益（占全店 GMV／Items 的比例）</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### 效益關係（由大到小）")
        st.markdown(
            """
<div class='nest-out'>
  <span class='nest-lab'>🏬 整店</span>
  <span class='nest-sub'>全店 GMV／Items Sold</span>
  <div class='nest-mid'>
    <span class='nest-lab'>🟪 深達整體</span>
    <span class='nest-sub'>深達帶來的 GMV／Items Sold　→　算「占整店多少 %」</span>
    <div class='nest-in'>
      <span class='nest-lab'>⭐ Top 10 深達</span>
      <span class='nest-sub'>算「占深達多少 %」與「占整店多少 %」</span>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.caption("一句話：月報要量化『深達占整店多少』，以及『Top 10 又占深達與整店多少』。")

        st.markdown(
            "<div class='ok'>💡 <b>不用手算</b>：可以用 <b>ChatGPT 或 Claude 幫忙寫程式碼</b>來分析。"
            "把當月深達／全店的 GMV、Items Sold 匯出檔丟給 AI，請它算出總計、排出 Top 10、"
            "以及各項占比，省時又不容易出錯。</div>",
            unsafe_allow_html=True,
        )

    with tab4:
        st.subheader("什麼是觸達")
        st.markdown(
            "把表現好的廣達轉成深達（**深達二次合作**）。"
            "先判斷達人分層，再發對應話術，最後更新兩張表的狀態。"
        )

        st.subheader("① 分層判斷（依近 28 天 affiliate orders）")
        st.markdown(
            "<div class='card'>"
            "• <b>10–28 單</b>（偶爾出單）＝ <b>T2S / T1</b> → 用「<b>2–3 款</b>」話術<br>"
            "• <b>28 單以上</b> ＝ <b>T0</b> → 用「<b>3–4 款</b>」話術<br>"
            "<span class='muted'>判斷依據都看「近 28 天」的 affiliate orders。</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.subheader("② 觸達步驟")
        st.markdown(
            "<div class='step'>1. 找到合適的廣達，找出他的<b>聯繫方式</b></div>"
            "<div class='step'>2. 發對應分層的<b>話術</b>給他（見下）</div>"
            "<div class='step'>3. 在<b>廣達表</b>把該達人狀態改成「<b>深達二次合作</b>」</div>"
            "<div class='step'>4. 在<b>深達表</b>把剛觸達的 <b>handle 填進去</b></div>"
            "<div class='step'>5. 在深度達人 <b>status 改成「優先－已觸達」</b></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='ok'>完成以上 5 步，這位達人的觸達就完成了。</div>",
            unsafe_allow_html=True,
        )

        st.subheader("③ 觸達話術")
        st.markdown(
            "<div class='card'>每段話術內含對應的 Google 表單連結，達人點進去選款式：<br>"
            "• <b>T2S / T1</b> → 表單「<b>NailVesta New Drop</b>」（只能選 <b>2–3 款</b>）<br>"
            "• <b>T0</b> → 表單「<b>Nails selection</b>」（選 <b>3–4 款</b>）<br>"
            "<span class='muted'>達人填完表單後，接「📝 表單回覆 → 下單」分頁的流程。</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown("**T2S / T1（10–28 單，偶爾出單）— 選 2–3 款**")
        st.code(SHEN_OUTREACH_T1, language=None)
        st.markdown("**T0（28 單以上）— 選 3–4 款**")
        st.code(SHEN_OUTREACH_T0, language=None)

    with tab5:
        st.subheader("流程總覽")
        st.markdown(
            "達人填完 Google 表單後，回覆會自動進到 Google Sheet。"
            "這頁是「把回覆變成實際出貨」的流程：**進 Sheet → 對庫存 → 填深達表 → 開水單**。"
        )

        st.subheader("兩張表單")
        st.markdown(
            "<div class='card'>"
            "• <b>NailVesta New Drop</b>：只能選 2–3 款 → 給 <b>T2S / T1</b> 填<br>"
            "• <b>Nails selection</b>：選 3–4 款 → 給 <b>T0</b> 填<br>"
            "<span class='muted'>兩張表單的回覆都會進到 Google Sheet 的 Form_Responses 分頁。</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Sheet 欄位（達人填的資訊）")
        st.markdown(
            "Timestamp ｜ TikTok handle ｜ Full Name ｜ Full shipping address（含 city）｜ "
            "Nail size ｜ Fave 2–3 styles ｜ Best contact info（email / phone）｜ "
            "Questions and comments ｜ Score"
        )

        st.subheader("下單步驟")
        st.markdown(
            "<div class='step'>1. 打開 Google Sheet 的 <b>Form_Responses</b>，看達人填的資訊</div>"
            "<div class='step'>2. <b>逐一</b>把每位達人的資訊填到<b>深達表</b>裡</div>"
            "<div class='step'>3. <b>款式去庫存表對</b>（門檻見下方），確定有庫存才填</div>"
            "<div class='step'>4. 填完一行後，把該行<b>後面的白色框框填滿變成黃色</b>"
            "——這是標記「上次填到哪」，下次接著做不會重複</div>"
            "<div class='step'>5. 複製剛填那行的<b>深達 handle</b> → 貼到<b>水單表</b>的"
            "「<b>深度達人單</b>」分類，直接貼上</div>",
            unsafe_allow_html=True,
        )

        st.subheader("📦 庫存門檻")
        st.markdown(
            "<div class='ok'>"
            "• <b>深達</b>：款式庫存<b>低於 5 副不批</b><br>"
            "• <b>廣達</b>：款式庫存低於 10 副不批"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='warn'>⚠️ <b>貼進水單前，務必再確認款式正確</b>"
            "（款式、尺寸等）。<b>一旦入進去，庫存表就會跟著變動</b>，"
            "改起來很麻煩，所以下單前一定要再核對一次。</div>",
            unsafe_allow_html=True,
        )

    with tab6:
        st.caption(
            "深達的 Follow Up 多以 Email 發送，每段含主旨。深達沒有 2.0。"
        )
        for stage, subj, body, note in SHEN_FU:
            st.markdown(f"**Follow Up {stage}**　·　主旨：{subj}")
            st.code(body, language=None)
            if note:
                st.caption(note)

        st.markdown("---")
        st.subheader("Follow Up 3.0 — 影片反饋話術（依評級）")
        render_feedback_section(SHEN_FEEDBACK, "shen")
        st.caption("同一份反饋話術，也可在「⭐ 評級制度（3.0）」頁找到（標深達）。")


def render_grading():
    st.title("⭐ 評級制度（3.0）")
    st.markdown("評級金字塔：由上到下表現遞減。星級對應如下，**評完都要回反饋**。")

    st.markdown(
        "<span class='pill s'>S＝★★★ 三星</span>"
        "<span class='pill ak'>AK / AS / C＝★★ 二星</span>"
        "<span class='pill bk'>BK1–4＝★ 一星（有口播問題）</span>"
        "<span class='pill bs'>BS1–2＝★ 一星（無口播）</span>",
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown(
        "<div class='card'><h4>🟢 S — 最高評級</h4>"
        "優秀視頻，完全符合推廣要求。<br>"
        "<b>動作：誇達人 ＋ 要廣告碼 ＋ 要聯繫方式</b></div>"

        "<div class='card'><h4>🟡 AK / AS / C — 準 S，差一點</h4>"
        "符合推廣要求，有潛力（口播小問題）。<b>動作：誇達人、給反饋讓再發、要廣告碼。</b><br>"
        "・<b>AK</b>：有口播、沒露臉的準 S<br>"
        "・<b>AS</b>：沒口播、有露臉的準 S<br>"
        "・<b>C</b>：高級、美甲展示</div>"

        "<div class='card'><h4>🟠 BK1–BK4 — 有潛力（口播問題）</h4>"
        "・<b>BK1</b>：視頻 &gt; 60s<br>"
        "・<b>BK2</b>：產品拍攝不清<br>"
        "・<b>BK3</b>：視頻 &lt; 20s<br>"
        "・<b>BK4</b>：沒上手</div>"

        "<div class='card'><h4>🔴 BS1–BS2 — 無口播</h4>"
        "・<b>BS1</b>：無口播、沒上手<br>"
        "・<b>BS2</b>：無口播、沒賣點</div>",
        unsafe_allow_html=True,
    )

    st.subheader("額外特殊情況")
    st.markdown(
        "<div class='card'>"
        "<span class='pill sp'>T</span> 我們的指甲＋別人的鏈接 / 別人的指甲＋我們的鏈接 / 西語<br>"
        "<span class='pill sp'>Haul</span> 混合包裹影片<br>"
        "<span class='pill sp'>D</span> 刪視頻 → 讓達人重發<br>"
        "<span class='pill sp'>S（速投）</span> 若有影片內容一樣都評 S，再標注「速投」"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='ok'>🔼 <b>PC（可深達）</b>：達到 100（單）或觀感好的美女，"
        "即可同時標記為「<b>可深達</b>」，後續轉入深達流程。</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("📝 影片反饋話術（依評級）")
    st.markdown(
        "<span class='tag tag-guang'>廣達</span> 評完級後，到 Shop Chat 發送對應反饋話術。",
        unsafe_allow_html=True,
    )
    with st.expander("📎 B 類（BK / BS / Haul）共通規則 & 追碼話術"):
        st.markdown(
            "- 符合**深度合作標準**的 B 類達人，也要正常發反饋\n"
            "- 符合**廣告標準**的 B 類達人，發完 B 類話術後，加一句追碼話術 + 要聯繫方式\n"
            "- **普通** B 類達人，不主動要廣告碼\n"
            "- BK 評級／回覆**優先級為倒序**：BK4 > BK3 > BK2 > BK1"
        )
        st.markdown("**還沒發廣告碼**（先發「Ad Code 找碼圖解」——圖解在「💬 話術庫」頁——再附這段）：")
        st.code(GUANG_B_ADCODE_PENDING, language=None)
        st.markdown("**已發廣告碼**：")
        st.code(GUANG_B_ADCODE_DONE, language=None)
    render_feedback_section(GUANG_FEEDBACK, "grading_guang")

    st.markdown(
        "<span class='tag tag-shen'>深達</span> 深達評完級後的反饋話術（要碼／各評級），多以 Email 發送。",
        unsafe_allow_html=True,
    )
    render_feedback_section(SHEN_FEEDBACK, "grading_shen")
    st.caption("同一份反饋話術，也可在廣達／深達各自的「Follow Up」分頁找到。")


def script_block(title, body, note=""):
    st.markdown(f"**{title}**")
    st.code(body, language=None)
    if note:
        st.caption(note)


def render_scripts():
    st.title("💬 話術庫（複製即用）")
    st.markdown(
        "<div class='warn'>📌 通用原則：所有回覆保持<b>親切、專業、有活力</b>的語調，"
        "適當使用表情符號增加親和力，確保資訊清晰準確。"
        "不確定的對話可至：營銷部門 → 達人部門 → CU 回覆情境 查看。</div>",
        unsafe_allow_html=True,
    )
    st.caption("每段話術右上角有複製鈕，點一下就能複製。")

    script_block(
        "📥 收到 Code 回覆",
        "Got it! Thank you so much for collaborating with us, babe 💅💖 "
        "We're so happy to have you on board!",
    )
    script_block(
        "❓ 詢問 Free Sample（想合作）",
        "Hi love 💕 Thank you so much for reaching out 🩷 "
        "You can request a free sample directly through our TikTok Shop Creator Center "
        "by selecting that style and submitting your request.",
    )
    script_block(
        "📝 問步驟（怎麼申請樣品）",
        "Hi love 💕 of course! I'm happy to help 🥰✨\n"
        "Here's how you can request your free sample step by step 💅:\n"
        "1️⃣ Go to your TikTok Shop → Creator Center\n"
        "2️⃣ Tap \"Free Sample\" at the top\n"
        "3️⃣ In the search bar, type NailVesta 💅\n"
        "4️⃣ Choose the nail style you love and click Apply",
    )
    script_block(
        "🎉 歡迎新達人",
        "I'm so happy to have you join our little family — welcome to NailVesta 💅💕 "
        "I can't wait to see your video!",
    )
    script_block(
        "✅ 批准了",
        "Hi babe! I just approved your request — I can't wait to see your beautiful content 💅✨",
    )
    script_block(
        "✉️ 寄邀請",
        "Hi babe🩷 I just sent the invitation to you! When you request your free sample, "
        "please let me know so I can keep an eye out 💅✨ thank you babe!",
    )
    script_block(
        "⏳ 申樣達人拖延（催發片前的安撫）",
        "Hi love! 💖 Thank you so much for being willing to collaborate with us! "
        "Due to the large number of applications we're currently receiving, it might take "
        "a little bit of time to process, and I truly appreciate your patience. "
        "I'll try my best to make this as quick as possible.",
    )
    script_block(
        "🙅 不符合粉絲畫像 / 不符的達人",
        "Hi love! Thank you so much for kind words. I am so sorry about that—because we've had "
        "a high number of requests and limited sample stock right now, the platform has set some "
        "requirements like minimum average views 🥺. I truly hope we can work together in the "
        "future when things open up a bit more! 💖",
        note="紅字提示：可改用 followers 為由，看達人哪項沒符合再去調整說法。",
    )
    script_block(
        "🔁 達人想換款式",
        "Ok babe 🤍 I'll ship Floral Muse (M) to you — it's the fourth one in the picture. "
        "I think it's going to look so good on you 💅✨💕",
        note="操作：先看達人選的款式還有沒有庫存；若有，去『換貨表』與『總表』更改後再回覆。",
    )
    script_block(
        "📐 尺寸不符",
        "Hi babe 🥹💖 I'm so sorry the size wasn't a perfect fit, I know that can be frustrating. "
        "Since our sample stock is really limited right now, would you mind trying a little "
        "adjustment trick first?\n"
        "✨ Too loose: Use the provided file to carefully file down the edges until the nails "
        "fit your fingers better.\n"
        "✨ Too tight: Use a hair dryer to apply hot air to the bottom of the nails, then gently "
        "press and flatten the bottom part to widen them.\n"
        "Please give it a try and keep me updated. I'd love to know how it works out for you 💖",
    )
    script_block(
        "📌 爆單達人置頂（請求 pin 影片）",
        "Hi babe, your video is truly stunning and I'm honestly obsessed 🥹💗 if it's not too "
        "much trouble, would you mind pinning it on your profile? It lets more people see your "
        "beautiful look right away and can really help your views and followers grow — thank you "
        "so much, I appreciate you!",
    )
    script_block(
        "🌎 西語達人（暫不合作）",
        "Hi love! 💖 Thank you so much for your interest in working with us — we truly appreciate "
        "your support and beautiful energy! At the moment, we don't have any team members who "
        "speak Spanish, so we're not able to fully understand or evaluate Spanish-language content "
        "just yet 😢. We're still a small but growing brand, and we hope to expand our team in the "
        "future to include more language support! Once we have someone on the team who can support "
        "Spanish-speaking creators, we'd love to reach back out and explore a collab with you! "
        "Thank you again for understanding and for thinking of us ✨💕",
    )

    st.markdown("---")
    st.subheader("🔎 達人問 Ad Code 哪裡找")
    st.caption("達人問廣告碼在哪裡時，把下面這張「找碼圖解」傳給他，並附上這段話術。")
    img_path = first_existing(
        "ad_code.jpg", "ad code.jpg",
        "ad_code.jpeg", "ad code.jpeg",
        "ad_code.png", "ad code.png",
    )
    if img_path:
        st.image(img_path, caption="How to find your ad code", use_container_width=True)
    else:
        st.info("把 ad_code.jpg 放到 app.py 同一層（repo 根目錄）就會顯示這張找碼圖解。")
    script_block(
        "話術（搭配圖片一起傳）",
        "Hi love! 💖 Totally got you! Here's a quick step-by-step guide on how to find your ad "
        "code 👇✨ Just follow the steps in the image and you'll have it ready in no time!\n\n"
        "When you generate it, please set the code's lifespan to 365 days, then copy and send it "
        "over so I can boost your video with ads to help it reach even more people 💅\n\n"
        "Let me know if you get stuck anywhere — happy to help! 🫶",
    )


def render_logistics():
    st.title("📦 包裹狀態與水單")

    st.subheader("狀態更新規則")
    st.markdown(
        """
| 階段 | 合作日期 | 包裹狀態 | 操作時機 |
|---|---|---|---|
| **1.0 運送中** | 填「**今天**」 | 改為 **In Transit** | 發送 1.0 階段 |
| **2.0 已送達** | 兩天後（篩選合作日期為「**前天**」） | 改為 **Delivered** | 發送 2.0 階段 |
"""
    )
    st.markdown(
        "<div class='ok'>包裹狀態的準確更新是合作流程順暢的關鍵，直接影響後續的評級與反饋時程。</div>",
        unsafe_allow_html=True,
    )

    st.subheader("水單填寫要點")
    st.markdown(
        "<div class='card'>"
        "• 客速類型選「<b>達人補寄</b>」<br>"
        "• <b>Handle 與 Order ID 必須優先填寫</b><br>"
        "• 發貨備註需包含<b>完整姓名、電話和地址</b><br>"
        "• Product Name 填款式；<b>達人若沒特別指定，就按當初發貨的款式</b>填"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption("以上為廣達水單補寄的填法。")

    st.subheader("📋 跟達人要資訊")
    st.markdown(
        "<div class='step'>補寄前請達人提供：<b>姓名、電話、地址</b>。</div>"
        "<div class='step'><b>地址</b>可以用 AI 工具檢查格式是否正確"
        "（拼字、城市、州別縮寫、郵遞區號）再填單，避免寄錯。</div>",
        unsafe_allow_html=True,
    )

    st.subheader("🧾 水單表收件資訊標準格式")
    st.markdown(
        "<div class='card'>每筆<b>三行</b>：<br>"
        "1. 收件人姓名<br>"
        "2. 電話（含國碼，格式 <code>(+1)號碼</code>）<br>"
        "3. 完整地址：街道 + Apt / Bldg，城市，州，國家，郵遞區號</div>",
        unsafe_allow_html=True,
    )
    st.markdown("**範例**")
    st.code(
        "Jasmin Ordonez\n"
        "(+1)7373483260\n"
        "1006 Home Depot Way Apt 4306 Bldg 4, Bastrop, Texas, United States 78602",
        language=None,
    )


def render_links():
    st.title("🔗 常用連結與系統")

    st.subheader("📋 觸達表單（已填入）")
    st.markdown(
        "深達觸達時發給達人選款式用，回覆都進同一份 Google Sheet：\n"
        "- **NailVesta New Drop**（選 2–3 款，給 T2S / T1）：https://forms.gle/3jQ3ainsrEyqzXjJA\n"
        "- **Nails selection**（選 3–4 款，給 T0）：https://forms.gle/ZRYf2D2KWETX3n2y7"
    )

    st.subheader("🗂️ 系統 / 工具清單")
    st.markdown(
        "<div class='ok'>以下系統的實際網址詳見 <b>Canva</b> 交接文件："
        "<a href='https://www.canva.com/design/DAHDfOnYwRE/anQklS9Kp9Jg8NFn-dGebw/edit' "
        "target='_blank'>開啟 Canva ↗</a></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
| 系統 / 工具 | 用途 | 網址 |
|---|---|---|
| **廣告表** | 管理所有廣告素材與投放狀態 | 詳見 Canva |
| **換貨管理**（換貨話數、換貨表） | 換貨話術記錄與換貨表單查詢 | 詳見 Canva |
| **庫存表 / 廣達總表 / 深達總表** | 即時庫存查詢與達人總表管理 | 詳見 Canva |
| **批達人 / 評級 3.0 系統**（TikTok 系統） | 批達人申請與影片評級 | 詳見 Canva |
| **3.0 反饋話術 / 訂單查詢** | 反饋話術與達人 handle 訂單搜尋 | 詳見 Canva |
| **FAQ 問題整理** | 常見問題彙整 | 詳見 Canva |
| **達人日報 / 達人日報 SOP** | 日報填表規則與範例 | 詳見 Canva |
| **腳本拆解 / 爆款視頻例子** | 腳本拆解與爆款視頻範例 | 詳見 Canva |
| **Lark — Affiliate List / Affiliate Account** | 批達人、評級時的主要操作後台 | 詳見 Canva |
| **fastmoos** | 分析達人 GMV、均播、品類（深達建聯篩選用） | 詳見 Canva |
| **curva** | 廣達廣告表 approve（深達每日工作） | 詳見 Canva |
"""
    )

    st.subheader("📨 寄送 Invite 流程（Creator Center）")
    st.markdown(
        "<div class='step'>進入 <b>Affiliate Center</b> 介面 → 找到 <b>Find Creator</b> → "
        "貼上 handle → 往下拉找到 <b>Invite</b> → 點<b>最上面的連結</b> → 發送 Invite</div>",
        unsafe_allow_html=True,
    )


# =============================================================
# 路由
# =============================================================
ROUTES = {
    PAGES[0]: render_intro,
    PAGES[1]: render_glossary,
    PAGES[2]: render_schedule,
    PAGES[3]: render_guang,
    PAGES[4]: render_shen,
    PAGES[5]: render_grading,
    PAGES[6]: render_scripts,
    PAGES[7]: render_logistics,
    PAGES[8]: render_links,
}
ROUTES[page]()

st.sidebar.markdown("---")
st.sidebar.caption("整理自《國內達人組日常任務》與《深達工作》兩份文件 · v1")
