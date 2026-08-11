#!/usr/bin/env python3
"""Swap index.html's stylesheet for the light Contact Sheet theme."""

import pathlib
import re

CSS = """
  /* Contact sheet: warm paper ground, white frames, sprocket rails both edges. */
  :root{
    --paper:#edeae3;
    --paper-2:#e5e1d8;
    --card:#fdfcfa;
    --ink:#1c1a16;
    --ink-soft:#5d574c;
    --line:#d6d1c6;
    --line-strong:#a9a294;
    --rail:#2a2723;
    --dark:#211f1a;
    --red:#c1281b;
    --rail-w:46px;
  }
  *{box-sizing:border-box}
  html{background:var(--paper);}
  body{
    margin:0; background:var(--paper); color:var(--ink);
    font-family:Charter,Georgia,'Times New Roman',serif;
    font-size:17.5px; line-height:1.72;
    -webkit-font-smoothing:antialiased;
    padding:0 var(--rail-w);
    border-left:1px solid var(--rail); border-right:1px solid var(--rail);
  }
  .disp{
    font-family:'Avenir Next Condensed','Helvetica Neue',Helvetica,'Arial Narrow',Arial,sans-serif;
    text-transform:uppercase;
  }
  .mono{ font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace; }
  a{color:var(--ink); text-decoration:underline; text-decoration-color:var(--red);
    text-decoration-thickness:1px; text-underline-offset:4px;}
  a:hover{color:var(--red);}
  a:focus-visible,button:focus-visible{outline:2px solid var(--red); outline-offset:3px;}
  .wrap{max-width:1000px; margin:0 auto; padding:0 26px;}
  p{margin:0 0 14px; max-width:40em;}
  h3{margin:0 0 6px; font-size:16.5px; letter-spacing:.03em; font-weight:600;}

  /* sprocket rails, fixed to both edges */
  .rail{
    position:fixed; top:0; bottom:0; width:var(--rail-w); z-index:40;
    background-color:var(--rail);
    background-image:linear-gradient(180deg, var(--paper) 0 17px, transparent 17px 44px);
    background-size:20px 44px; background-repeat:repeat-y; background-position:center 10px;
    pointer-events:none;
  }
  .rail.l{left:0; border-right:1px solid #000;}
  .rail.r{right:0; border-left:1px solid #000;}
  .strip{display:none;}
  @media (max-width:880px){
    :root{--rail-w:16px;}
    .rail{background-image:none;}
  }

  /* top bar */
  nav.top{
    position:sticky; top:0; z-index:30; background:rgba(237,234,227,.96);
    border-bottom:1.5px solid var(--ink); backdrop-filter:blur(6px);
  }
  nav.top .wrap{display:flex; align-items:center; gap:22px; padding-top:13px; padding-bottom:13px; flex-wrap:wrap;}
  nav.top .brand{font-size:12px; letter-spacing:.3em; text-decoration:none; color:var(--ink);
    font-weight:600; margin-right:auto;}
  nav.top .brand b{color:var(--red);}
  nav.top a.nl{text-decoration:none; color:var(--ink-soft); font-size:10.5px; letter-spacing:.22em;}
  nav.top a.nl:hover{color:var(--red);}

  /* views */
  .view{display:none;}
  .view.active{display:block;}

  /* hero */
  header.hero{border-bottom:2.5px solid var(--ink);}
  .hero-grid{
    display:grid; grid-template-columns:minmax(0,1.5fr) minmax(260px,.9fr);
    gap:40px; padding-top:64px; padding-bottom:54px; align-items:end;
  }
  @media (max-width:760px){ .hero-grid{grid-template-columns:1fr; gap:28px;} }
  .eyebrow{font-size:11.5px; letter-spacing:.34em; color:var(--ink-soft); margin:0 0 26px;}
  .eyebrow b{color:var(--red); font-weight:600;}
  h1{margin:0; font-weight:700; letter-spacing:.005em;
    font-size:clamp(46px,9vw,104px); line-height:.92; text-wrap:balance;}
  h1 .ln{display:block;}
  h1 .hollow{color:transparent; -webkit-text-stroke:1.5px var(--ink);}
  @supports not (-webkit-text-stroke:1px #000){ h1 .hollow{color:var(--red);} }
  .lede{max-width:33em; margin:30px 0 0; font-size:19px;}
  .lede em{color:var(--ink-soft); font-style:italic;}
  .cta-row{display:flex; gap:14px; flex-wrap:wrap; margin-top:30px;}
  .cta{display:inline-block; text-decoration:none; font-size:11px; letter-spacing:.24em;
    padding:13px 20px 12px; border:1.5px solid var(--red); color:var(--red); background:var(--card);}
  .cta.solid{background:var(--red); color:#fff;}
  .cta:hover{background:var(--red); color:#fff;}

  .callsheet{border:1.5px solid var(--ink); background:var(--card); font-size:12px; letter-spacing:.06em;}
  .callsheet .cs-title{padding:9px 14px; border-bottom:1.5px solid var(--ink);
    color:var(--red); letter-spacing:.3em; font-size:10.5px; background:var(--paper-2);}
  .callsheet dl{margin:0; display:grid; grid-template-columns:auto 1fr;}
  .callsheet dt{padding:11px 14px; color:var(--ink-soft); border-bottom:1px solid var(--line);
    letter-spacing:.2em; font-size:10px; align-self:center;}
  .callsheet dd{margin:0; padding:11px 14px 11px 0; border-bottom:1px solid var(--line);
    color:var(--ink); text-align:right;}
  .callsheet dt:last-of-type, .callsheet dd:last-of-type{border-bottom:none;}

  /* tenets */
  .tenets{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
    gap:1px; background:var(--line-strong); border:1.5px solid var(--ink); margin-top:60px;}
  .tenet{background:var(--card); padding:22px 22px 18px;}
  .tenet .tn{color:var(--red); font-size:10.5px; letter-spacing:.3em; display:block; margin-bottom:10px;}
  .tenet p{margin:0; font-size:17px; line-height:1.55; max-width:none;}

  /* sections */
  section{padding:72px 0 6px;}
  .sec-head{display:flex; align-items:center; gap:18px; margin-bottom:12px;}
  .fr{flex:none; border:1.5px solid var(--red); color:var(--red); background:var(--card);
    font-size:11px; letter-spacing:.18em; padding:5px 9px 4px;}
  h2{margin:0; font-size:clamp(24px,3.4vw,34px); font-weight:700;
    letter-spacing:.02em; text-wrap:balance; line-height:1.05;}
  .sec-head::after{content:""; flex:1; height:1.5px; background:var(--ink); min-width:40px;}
  .sec-sub{color:var(--ink-soft); max-width:42em; margin:0 0 34px; font-size:17px;}

  /* semester map cards */
  .sessions{display:grid; grid-template-columns:repeat(auto-fill,minmax(252px,1fr)); gap:14px;}
  .scard{border:1px solid var(--line-strong); background:var(--card); padding:16px 16px 14px;
    display:flex; flex-direction:column; gap:9px; text-decoration:none; color:var(--ink);}
  a.scard:hover{border-color:var(--ink); color:var(--ink);}
  .scard.live{border:2px solid var(--red);}
  .scard .sn{color:var(--ink-soft); font-size:10.5px; letter-spacing:.26em;}
  .scard.live .sn{color:var(--red);}
  .scard h3{font-size:15px; letter-spacing:.04em; margin:0; line-height:1.3;}
  .scard .row{font-size:13.5px; color:var(--ink-soft); margin:0; line-height:1.55; max-width:none;}
  .scard .row b{color:var(--ink); font-size:9.5px; letter-spacing:.2em; margin-right:7px; font-weight:600;}
  .status{margin-top:auto; align-self:flex-start; font-size:9.5px; letter-spacing:.22em;
    padding:5px 9px 4px; border:1px solid var(--line-strong); color:var(--ink-soft);}
  .scard.live .status{border-color:var(--red); color:#fff; background:var(--red);}

  /* flow */
  ol.flow{list-style:none; margin:0; padding:0; border-top:1.5px solid var(--ink);}
  ol.flow li{display:grid; grid-template-columns:70px 190px 1fr; gap:20px;
    padding:16px 0; border-bottom:1px solid var(--line); align-items:baseline;}
  ol.flow .n{color:var(--red); font-size:12px; letter-spacing:.14em;}
  ol.flow .st{font-size:12.5px; letter-spacing:.24em; color:var(--ink); font-weight:600;}
  ol.flow .d{color:var(--ink-soft); font-size:16px; max-width:none; font-family:Charter,Georgia,serif;}
  ol.flow .d b{color:var(--ink); font-weight:600;}
  ol.flow li.today{background:linear-gradient(90deg, rgba(193,40,27,.10), transparent 70%);}
  ol.flow li.today .st{color:var(--red);}
  @media (max-width:640px){
    ol.flow li{grid-template-columns:56px 1fr;}
    ol.flow .d{grid-column:2;}
  }

  /* panels */
  .grid2{display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:22px;}
  .grid3{display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:22px;}
  .panel{background:var(--card); border:1px solid var(--line-strong); padding:22px 22px 16px;}
  .tag{display:inline-block; color:var(--red); font-size:10.5px; letter-spacing:.3em; margin-bottom:14px;}
  .panel ul{margin:0; padding-left:16px;}
  .panel li{margin-bottom:10px; font-size:16px; color:var(--ink); line-height:1.6;}
  .panel li::marker{color:var(--red);}

  /* session hero + subnav */
  .s-hero{border-bottom:2.5px solid var(--ink);}
  .s-hero .hero-grid{padding-top:52px; padding-bottom:44px;}
  .s-hero h1{font-size:clamp(36px,6.4vw,74px);}
  .crumb{margin:0 0 22px; font-size:10.5px; letter-spacing:.26em;}
  .crumb a{color:var(--ink-soft); text-decoration:none;}
  .crumb a:hover{color:var(--red);}
  .crumb .sep{color:var(--red); margin:0 8px;}

  nav.sub{border-bottom:1px solid var(--line-strong); background:var(--paper-2);}
  nav.sub .wrap{display:flex; gap:0 24px; flex-wrap:wrap; padding-top:11px; padding-bottom:11px;}
  nav.sub a{text-decoration:none; color:var(--ink-soft); font-size:10.5px; letter-spacing:.2em;}
  nav.sub a:hover{color:var(--red);}
  nav.sub .sep{color:var(--red); font-size:10px; letter-spacing:.2em;}

  /* part divider: dark frame separator */
  .part{border:1.5px solid var(--ink); background:var(--dark); color:#f1ede4;
    padding:30px 34px 26px; margin-top:86px; position:relative;}
  .part::before,.part::after{content:""; position:absolute; width:18px; height:18px;}
  .part::before{top:-1px; left:-1px; border-top:3px solid var(--red); border-left:3px solid var(--red);}
  .part::after{bottom:-1px; right:-1px; border-bottom:3px solid var(--red); border-right:3px solid var(--red);}
  .part .p-eyebrow{color:var(--red); font-size:10.5px; letter-spacing:.36em; margin:0 0 10px;}
  .part h2{font-size:clamp(24px,3.6vw,38px); color:#f8f5ee;}
  .part p{color:#b9b2a4; font-size:16px; margin:12px 0 0; max-width:44em;}

  /* case cards: proof frames */
  .cases{display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:22px;}
  .case{background:var(--dark); border:1px solid var(--ink); padding:7px;}
  .case-inner{border:1px solid var(--line-strong); padding:18px 18px 14px; height:100%;
    display:flex; flex-direction:column; gap:11px; background:var(--card);}
  .case .id{display:flex; justify-content:space-between; align-items:baseline;
    color:var(--ink-soft); font-size:10.5px; letter-spacing:.24em;}
  .case .id .frn{color:var(--red);}
  .case .pair{margin:0; display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;}
  .case .pair a{font-size:19px; font-weight:700; letter-spacing:.05em; text-decoration:none;
    color:var(--ink); border-bottom:2.5px solid var(--red); padding-bottom:1px;}
  .case .pair a:hover{color:var(--red);}
  .case .pair .x{color:var(--ink-soft); font-size:11px; letter-spacing:.2em;}
  .case p.read{font-size:15.5px; color:var(--ink); margin:0; max-width:none; line-height:1.6;}
  .case p.read a{color:var(--ink-soft);}
  .case .lesson{margin-top:auto; padding-top:10px; border-top:1px dashed var(--line-strong);
    color:var(--ink-soft); font-size:14px;}
  .case .lesson b{color:var(--red); font-weight:600; letter-spacing:.18em; font-size:10px; margin-right:8px;}

  /* framework layers */
  .layers{display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
    gap:1px; background:var(--line-strong); border:1.5px solid var(--ink);}
  .layer{background:var(--card); padding:22px 20px 18px;}
  .layer .lt{display:block; color:var(--red); font-size:10.5px; letter-spacing:.3em; margin-bottom:12px;}
  .layer p{color:var(--ink-soft); font-size:15.5px; margin:0; max-width:none; line-height:1.6;}

  /* persona sentence */
  .sentence{position:relative; background:var(--card); border:1px solid var(--line-strong);
    padding:34px 38px; max-width:46em; margin:8px 0 20px;
    font-size:clamp(20px,2.6vw,26px); line-height:1.55; font-style:italic;}
  .sentence .slot{color:var(--red); font-style:normal; font-weight:600;}
  .sentence::before,.sentence::after{content:""; position:absolute; width:16px; height:16px;}
  .sentence::before{top:-1px; left:-1px; border-top:3px solid var(--red); border-left:3px solid var(--red);}
  .sentence::after{bottom:-1px; right:-1px; border-bottom:3px solid var(--red); border-right:3px solid var(--red);}

  /* apply boxes: grease-pencil note */
  .apply{border:1px solid var(--line-strong); border-left:4px solid var(--red);
    background:var(--card); padding:15px 20px; margin:30px 0 0; font-size:16px; max-width:46em;}
  .apply b{color:var(--red); font-size:10px; letter-spacing:.26em; margin-right:14px; font-weight:600;}

  /* handout + tool blocks */
  .handout{border:1.5px solid var(--ink); background:var(--card); padding:22px 24px 20px;
    margin:0 0 34px; display:flex; gap:26px; align-items:center; flex-wrap:wrap;}
  .handout .ht{flex:1 1 330px;}
  .handout .he{color:var(--red); font-size:10.5px; letter-spacing:.3em; display:block; margin-bottom:8px;}
  .handout h3{font-size:19px; margin:0 0 7px; letter-spacing:.03em;}
  .handout p{margin:0; color:var(--ink-soft); font-size:15.5px; max-width:44em;}
  .dl{display:flex; gap:12px; flex-wrap:wrap;}
  a.dlbtn{display:inline-block; text-decoration:none; border:1.5px solid var(--red); color:var(--red);
    background:var(--card); font-size:11px; letter-spacing:.2em; padding:12px 18px 11px;
    white-space:nowrap; text-align:center;}
  a.dlbtn:hover{background:var(--red); color:#fff;}
  a.dlbtn span{display:block; font-size:9px; letter-spacing:.12em; color:var(--ink-soft); margin-top:4px;}
  a.dlbtn:hover span{color:rgba(255,255,255,.78);}
  a.dlbtn.solid{background:var(--red); color:#fff;}
  a.dlbtn.solid span{color:rgba(255,255,255,.75);}
  a.dlbtn.solid:hover{background:#a52114; border-color:#a52114;}

  .toolref{border:1px solid var(--line-strong); border-left:4px solid var(--red); background:var(--card);
    padding:20px 22px 18px; margin-top:24px; display:flex; gap:22px; align-items:center; flex-wrap:wrap;}
  .toolref .tr{flex:1 1 340px;}
  .toolref .tt{color:var(--red); font-size:10px; letter-spacing:.28em; display:block; margin-bottom:8px;}
  .toolref h3{margin:0 0 7px; font-size:17.5px; letter-spacing:.03em;}
  .toolref p{margin:0; color:var(--ink-soft); font-size:15.5px; max-width:48em;}

  /* ladder */
  .ladder{list-style:none; margin:0; padding:0;}
  .ladder>li{border:1px solid var(--line-strong); background:var(--card);
    padding:26px 28px 22px; margin-bottom:22px;}
  .ladder>li.gate{border-left:4px solid var(--red);}
  .l-top{display:flex; align-items:baseline; gap:18px; flex-wrap:wrap; margin-bottom:10px;}
  .l-step{color:var(--red); font-size:11px; letter-spacing:.28em;}
  .l-top h3{font-size:20px; margin:0; letter-spacing:.03em;}
  .l-build{margin:0 0 10px; color:var(--ink-soft); font-size:16px; max-width:none;}
  .l-build b{color:var(--ink); font-size:10px; letter-spacing:.22em; margin-right:12px; font-weight:600;}
  .l-meta{display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; margin-top:16px;}
  .l-meta .m{border-top:1px solid var(--line); padding-top:12px; font-size:15.5px;
    color:var(--ink); line-height:1.6;}
  .l-meta .m b{display:block; color:var(--red); font-size:10px; letter-spacing:.24em;
    margin-bottom:8px; font-weight:600;}

  /* prompts: dark slate on paper */
  .stage{margin-bottom:34px;}
  .stage h3{font-size:15px; letter-spacing:.22em; font-weight:600;}
  .stage h3 .n{color:var(--red); margin-right:10px;}
  pre.prompt{background:var(--dark); color:#efe9dd; border:1px solid var(--ink);
    border-left:4px solid var(--red); padding:18px 20px; font-size:13.5px; line-height:1.65;
    overflow-x:auto; margin:12px 0 8px; white-space:pre-wrap; word-break:break-word;}
  .stage .note{color:var(--ink-soft); font-size:15px; max-width:44em;}

  /* recipes */
  .recipe{background:var(--card); border:1px solid var(--line-strong);
    border-top:3px solid var(--red); padding:20px 20px 14px;}
  .recipe .rt{color:var(--red); font-size:10.5px; letter-spacing:.3em; display:block; margin-bottom:10px;}
  .recipe h3{font-size:17px;}
  .recipe dl{margin:12px 0 0; display:grid; grid-template-columns:88px 1fr; gap:8px 12px; font-size:13.5px;}
  .recipe dt{color:var(--ink-soft); letter-spacing:.14em; font-size:10px; padding-top:4px;}
  .recipe dd{margin:0; color:var(--ink); font-family:Charter,Georgia,serif; font-size:15px; line-height:1.55;}

  /* tables */
  .tablewrap{overflow-x:auto; border:1.5px solid var(--ink);}
  table{width:100%; border-collapse:collapse; font-size:15.5px; background:var(--card);}
  th,td{text-align:left; padding:14px 16px; border-bottom:1px solid var(--line); vertical-align:top;}
  th{font-size:10.5px; letter-spacing:.26em; color:#e9e3d7; font-weight:600;
    text-transform:uppercase; background:var(--dark);}
  tr:last-child td{border-bottom:none;}
  td.trend{white-space:nowrap; font-weight:700; letter-spacing:.04em; font-size:14px;}
  td{color:var(--ink);}
  td p{margin:0; max-width:none; font-size:15.5px; color:var(--ink-soft); line-height:1.6;}

  /* placeholder view */
  .ph{padding:88px 0 40px;}
  .ph .sn{color:var(--red); font-size:12px; letter-spacing:.3em;}
  .ph h1{font-size:clamp(34px,6vw,62px); margin:14px 0 20px;}
  .ph .row{color:var(--ink-soft); font-size:16.5px; margin:0 0 8px; max-width:40em;}
  .ph .row b{color:var(--ink); font-size:10px; letter-spacing:.22em; margin-right:10px;}
  .ph .status{margin-top:26px; display:inline-block;}
  .ph .back{margin-top:40px;}

  footer{border-top:2.5px solid var(--ink); margin-top:80px; background:var(--paper-2);}
  footer .wrap{padding:26px 26px 34px; display:flex; flex-wrap:wrap; gap:6px 32px;
    font-size:10.5px; letter-spacing:.24em; color:var(--ink-soft);}
  footer .wrap span:first-child{color:var(--ink);}
"""

page = pathlib.Path(__file__).parent / "index.html"
html = page.read_text()

new, n = re.subn(r"<style>.*?</style>", f"<style>{CSS}</style>", html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("style block not found")

# swap the old top strip for the two sprocket rails
new, n2 = re.subn(
    r'<div class="strip" aria-hidden="true"></div>',
    '<div class="rail l" aria-hidden="true"></div>\n<div class="rail r" aria-hidden="true"></div>',
    new,
    count=1,
)
if n2 != 1:
    raise SystemExit("strip div not found")

page.write_text(new)
print(f"restyled; index.html is {len(new)/1024:.0f} KB")
