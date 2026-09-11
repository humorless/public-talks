import math

W, H = 952, 404
L, R = 96, 700          # plot x range
TOP, BOT = 48, 322      # plot y range (svg coords)

def human(t):   return 0.43 * (1 - math.exp(-9 * t)) + 0.03
def compute(t): return 0.015 + 0.92 * (t ** 1.4)

def X(t): return L + t * (R - L)
def Y(v): return BOT - v * (BOT - TOP) / 1.0

def path(f, n=220):
    pts = [(X(i / n), Y(f(i / n))) for i in range(n + 1)]
    return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)

# crossover
lo, hi = 0.0, 1.0
for _ in range(60):
    mid = (lo + hi) / 2
    if compute(mid) < human(mid): lo = mid
    else: hi = mid
tc = (lo + hi) / 2
cx, cy = X(tc), Y(human(tc))

FONT = "'PingFang TC','Heiti TC','Noto Sans CJK TC',sans-serif"
BLUE, AMBER, GREY = "#4a90d9", "#d9a017", "#999999"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <marker id="ax" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
    <path d="M0,1 L8,4.5 L0,8 z" fill="#bbbbbb"/>
  </marker>
  <marker id="pt" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
    <path d="M0,1 L7,4 L0,7 z" fill="#666666"/>
  </marker>
</defs>
<style>
  text {{ font-family: {FONT}; }}
  .lbl {{ font-size: 21px; font-weight: 600; }}
  .sub {{ font-size: 15px; }}
  .ax  {{ font-size: 15px; fill: #888888; }}
  .zone{{ font-size: 17px; font-weight: 600; }}
</style>

<!-- crossover shading -->
<rect x="{cx:.1f}" y="{TOP-8}" width="{R-cx+34:.1f}" height="{BOT-TOP+8}" fill="{BLUE}" opacity="0.05"/>

<!-- axes -->
<line x1="{L}" y1="{BOT}" x2="{R+52}" y2="{BOT}" stroke="#bbbbbb" stroke-width="1.5" marker-end="url(#ax)"/>
<line x1="{L}" y1="{BOT}" x2="{L}" y2="{TOP-16}" stroke="#bbbbbb" stroke-width="1.5" marker-end="url(#ax)"/>
<text class="ax" x="{R+56}" y="{BOT+52}" text-anchor="end">算力 × 時間</text>
<text class="ax" x="{L-10}" y="{TOP-20}" text-anchor="middle">能力</text>

<!-- zone divider -->
<line x1="{cx:.1f}" y1="{BOT}" x2="{cx:.1f}" y2="{TOP-8}" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="5,5"/>
<text class="zone" x="{(L+cx)/2:.1f}" y="{BOT+26:.1f}" text-anchor="middle" fill="{AMBER}">短期：手寫知識領先</text>
<text class="zone" x="{(cx+R+40)/2:.1f}" y="{BOT+26:.1f}" text-anchor="middle" fill="{BLUE}">長期：通用方法碾壓</text>

<!-- curves -->
<path d="{path(human)}" fill="none" stroke="{AMBER}" stroke-width="3.4" stroke-linecap="round"/>
<path d="{path(compute)}" fill="none" stroke="{BLUE}" stroke-width="4.2" stroke-linecap="round"/>

<!-- crossover marker -->
<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6.5" fill="#ffffff" stroke="#1a1a2e" stroke-width="2.4"/>
<line x1="{cx-58:.1f}" y1="{cy-56:.1f}" x2="{cx-9:.1f}" y2="{cy-11:.1f}" stroke="#666666" stroke-width="1.3" marker-end="url(#pt)"/>
<text class="lbl" x="{cx-62:.1f}" y="{cy-64:.1f}" text-anchor="end" fill="#1a1a2e">交叉點</text>
<text class="sub" x="{cx-62:.1f}" y="{cy-45:.1f}" text-anchor="end" fill="#666666">手寫知識開始被碾壓</text>

<!-- curve labels -->
<text class="lbl" x="{R+16}" y="{Y(compute(1.0))+2:.1f}" fill="{BLUE}">通用方法 + 算力</text>
<text class="sub" x="{R+16}" y="{Y(compute(1.0))+22:.1f}" fill="{BLUE}">search + learning</text>
<text class="lbl" x="{R+16}" y="{Y(human(1.0))+2:.1f}" fill="{AMBER}">人類手寫的領域知識</text>
<text class="sub" x="{R+16}" y="{Y(human(1.0))+22:.1f}" fill="{AMBER}">硬編碼規則、專門特徵</text>
</svg>
'''
open("/Users/laurencechen/Downloads/cowork/jcconf/images/bitter-lesson.svg", "w").write(svg)
print(f"crossover t={tc:.3f} at x={cx:.1f} y={cy:.1f}")

# 產圖：
#   python3 images/bitter-lesson.py
#   rsvg-convert -z 1.5625 images/bitter-lesson.svg -o images/bitter-lesson.png
