/* LinguaGo 前端单页应用 */
"use strict";

/* ================= 基础工具 ================= */
const LANG_META = {
    en: { name: "英语", flag: "🇺🇸", locale: "en-US" },
    ja: { name: "日语", flag: "🇯🇵", locale: "ja-JP" },
    ko: { name: "韩语", flag: "🇰🇷", locale: "ko-KR" },
};
const TYPE_META = {
    vocabulary: { label: "单词记忆", icon: "📇", color: "#6366f1" },
    grammar: { label: "语法练习", icon: "📖", color: "#8b5cf6" },
    speaking: { label: "口语跟读", icon: "🎤", color: "#ec4899" },
    listening: { label: "听力训练", icon: "🎧", color: "#14b8a6" },
};

const $ = (sel) => document.querySelector(sel);
const appEl = () => document.getElementById("app");

function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
}
function fmtTime(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return "";
    return d.toLocaleString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(t._t);
    t._t = setTimeout(() => t.classList.remove("show"), 2400);
}

/* ================= 认证状态 ================= */
let TOKEN = localStorage.getItem("lingua_token") || "";
let USER = JSON.parse(localStorage.getItem("lingua_user") || "null");

function setAuth(token, user) {
    TOKEN = token;
    USER = user;
    localStorage.setItem("lingua_token", token);
    localStorage.setItem("lingua_user", JSON.stringify(user));
}
function clearAuth() {
    TOKEN = "";
    USER = null;
    localStorage.removeItem("lingua_token");
    localStorage.removeItem("lingua_user");
}

/* ================= API ================= */
async function api(path, opts = {}) {
    const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
    if (TOKEN) headers["Authorization"] = "Bearer " + TOKEN;
    const res = await fetch("/api" + path, { ...opts, headers });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
        if (res.status === 401) {
            clearAuth();
            if (location.hash.split("?")[0] !== "#/login") location.hash = "#/login";
        }
        throw new Error(data.detail || "请求失败");
    }
    return data;
}

/* ================= 语音能力 ================= */
function speak(text, lang) {
    return new Promise((resolve, reject) => {
        if (!("speechSynthesis" in window)) return reject(new Error("浏览器不支持语音合成"));
        const u = new SpeechSynthesisUtterance(text);
        u.lang = (LANG_META[lang] || LANG_META.en).locale;
        u.rate = 0.9;
        u.onend = resolve;
        u.onerror = reject;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
    });
}

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
function speechAvailable() { return !!SR; }

function recognize(lang) {
    return new Promise((resolve, reject) => {
        if (!SR) return reject(new Error("当前浏览器不支持语音识别，请使用 Chrome"));
        const rec = new SR();
        rec.lang = (LANG_META[lang] || LANG_META.en).locale;
        rec.interimResults = false;
        rec.maxAlternatives = 1;
        rec.onresult = (e) => resolve(e.results[0][0].transcript);
        rec.onerror = (e) => reject(new Error("识别失败：" + e.error));
        rec.onend = () => { if (!rec._res) resolve(""); };
        rec.onresult = (e) => { rec._res = true; };
        rec.start();
    });
}

function similarity(a, b) {
    const norm = (s) => s.toLowerCase().replace(/[.,!?]/g, "").split(/\s+/).filter(Boolean);
    const ta = new Set(norm(a)), tb = new Set(norm(b));
    if (!ta.size || !tb.size) return 0;
    let inter = 0;
    ta.forEach((x) => { if (tb.has(x)) inter++; });
    return Math.min(100, Math.round((inter / ta.size) * 100));
}

/* ================= 路由 ================= */
const routes = {
    "#/login": viewAuth,
    "#/register": viewAuth,
    "#/home": viewHome,
    "#/courses": viewCourses,
    "#/course/": viewCourse,
    "#/lesson/": viewLesson,
    "#/progress": viewProgress,
    "#/community": viewCommunity,
    "#/post/": viewPost,
    "#/achievements": viewAchievements,
    "#/profile": viewProfile,
};

function currentRoute() {
    const h = location.hash || "#/home";
    for (const key of Object.keys(routes)) {
        if (key.endsWith("/") && h.startsWith(key)) return { fn: routes[key], param: h.slice(key.length) };
        if (h === key) return { fn: routes[key], param: null };
    }
    return { fn: viewHome, param: null };
}

function navigate(hash) { location.hash = hash; }

async function render() {
    const { fn, param } = currentRoute();
    if (!TOKEN && !["#/login", "#/register"].includes(location.hash.split("?")[0])) {
        location.hash = "#/login";
        return;
    }
    if (TOKEN && ["#/login", "#/register"].includes(location.hash.split("?")[0])) {
        location.hash = "#/home";
        return;
    }
    await fn(param);
}

window.addEventListener("hashchange", render);

/* ================= 认证视图 ================= */
async function viewAuth() {
    const mode = location.hash.startsWith("#/register") ? "register" : "login";
    appEl().innerHTML = `
    <div class="auth-screen">
        <div class="auth-left">
            <h1>LinguaGo</h1>
            <p>沉浸式多语种学习平台，涵盖英语、日语、韩语。分级课程 + 互动练习 + 进度追踪 + 成就激励，让学习更有趣。</p>
            <div class="auth-flags">🇺🇸 🇯🇵 🇰🇷</div>
        </div>
        <div class="auth-right">
            <div class="auth-card">
                <h2>${mode === "login" ? "欢迎回来" : "创建账号"}</h2>
                <div class="sub">${mode === "login" ? "登录后继续你的学习旅程" : "开启你的多语种学习之旅"}</div>
                <div class="auth-tabs">
                    <button data-mode="login" class="${mode === "login" ? "active" : ""}">登录</button>
                    <button data-mode="register" class="${mode === "register" ? "active" : ""}">注册</button>
                </div>
                <form id="auth-form">
                    ${mode === "register" ? `
                    <div class="field"><label>用户名</label><input name="username" required minlength="2" maxlength="24" /></div>` : ""}
                    <div class="field"><label>邮箱</label><input name="email" type="email" required /></div>
                    <div class="field"><label>密码</label><input name="password" type="password" required minlength="6" /></div>
                    ${mode === "register" ? `
                    <div class="field"><label>母语</label>
                        <select name="native_language">
                            <option value="zh">中文</option><option value="en">English</option>
                            <option value="ja">日本語</option><option value="ko">한국어</option>
                        </select>
                    </div>
                    <div class="field"><label>想学习的语言（可多选）</label>
                        <div class="chip-group" id="lang-chips">
                            <button type="button" class="chip active" data-lang="en">英语 🇺🇸</button>
                            <button type="button" class="chip" data-lang="ja">日语 🇯🇵</button>
                            <button type="button" class="chip" data-lang="ko">韩语 🇰🇷</button>
                        </div>
                    </div>` : ""}
                    <button type="submit" class="btn btn-primary btn-block mt2">${mode === "login" ? "登录" : "注册并开始学习"}</button>
                </form>
            </div>
        </div>
    </div>`;

    document.querySelectorAll(".auth-tabs button").forEach((b) => {
        b.onclick = () => navigate(b.dataset.mode === "login" ? "#/login" : "#/register");
    });
    if (mode === "register") {
        document.querySelectorAll("#lang-chips .chip").forEach((c) => {
            c.onclick = () => c.classList.toggle("active");
        });
    }
    $("#auth-form").onsubmit = async (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        const payload = { email: fd.get("email"), password: fd.get("password") };
        if (mode === "register") {
            payload.username = fd.get("username");
            payload.native_language = fd.get("native_language");
            payload.target_languages = [...document.querySelectorAll("#lang-chips .chip.active")].map((c) => c.dataset.lang);
        }
        const btn = e.target.querySelector("button[type=submit]");
        btn.disabled = true;
        try {
            const data = await api(mode === "login" ? "/auth/login" : "/auth/register", {
                method: "POST", body: JSON.stringify(payload),
            });
            setAuth(data.token, data.user);
            toast(mode === "login" ? "登录成功" : "注册成功");
            navigate("#/home");
        } catch (err) {
            toast(err.message);
        } finally { btn.disabled = false; }
    };
}

/* ================= 应用外壳 ================= */
function shell(title, content, activeNav) {
    const items = [
        ["#/home", "🏠", "首页", "home"],
        ["#/courses", "📚", "课程", "courses"],
        ["#/progress", "📈", "学习进度", "progress"],
        ["#/community", "💬", "社区", "community"],
        ["#/achievements", "🏆", "成就", "achievements"],
    ];
    const nav = items.map(([h, ico, label, key]) =>
        `<a href="${h}" class="${activeNav === key ? "active" : ""}"><span class="ico">${ico}</span>${label}</a>`
    ).join("");
    const initial = (USER?.username || "U")[0].toUpperCase();
    appEl().innerHTML = `
    <div class="app">
        <aside class="sidebar">
            <div class="brand"><div class="logo">L</div><div class="name">Lingua<span>Go</span></div></div>
            <nav class="nav">${nav}
                <a href="#/profile" class="${activeNav === "profile" ? "active" : ""}"><span class="ico">⚙️</span>设置</a>
            </nav>
            <div class="user-box">
                <div class="top"><div class="avatar">${esc(initial)}</div>
                    <div><div class="name">${esc(USER?.username)}</div><div class="meta">${esc(USER?.level)} 水平</div></div>
                </div>
                <div class="stat-row">
                    <div class="s"><b>🔥 ${USER?.streak ?? 0}</b><span>连续天数</span></div>
                    <div class="s"><b>💎 ${USER?.points ?? 0}</b><span>积分</span></div>
                </div>
            </div>
        </aside>
        <main class="main">
            <div class="topbar">
                <h1>${title}</h1>
                ${USER ? `<div class="streak-pill">🔥 连续 ${USER.streak} 天</div>` : ""}
            </div>
            ${content}
        </main>
    </div>`;
}

function avgColor(hex) { return hex || "#6366f1"; }
function progressBar(done, total) {
    const pct = total ? Math.round(done * 100 / total) : 0;
    return `<div class="cc-bar"><div style="width:${pct}%"></div></div>`;
}

/* ================= 首页 ================= */
async function viewHome() {
    let rec, prog;
    try {
        [rec, prog] = await Promise.all([api("/recommendations"), api("/progress")]);
    } catch (e) { return toast(e.message); }
    const s = prog.stats;
    const next = rec.next_lessons || [];
    const review = rec.review || [];

    const nextHtml = next.slice(0, 3).map((n) => `
        <div class="card pad-sm course-card" onclick="navigate('#/lesson/${n.lesson_id}')">
            <div class="cc-head">
                <div class="cc-icon" style="background:${avgColor(n.course_color)}">${n.course_icon}</div>
                <div><div class="cc-title">${esc(n.lesson_title)}</div>
                    <div class="muted" style="font-size:12.5px">${n.language_name} · ${esc(n.lesson_type)}</div></div>
            </div>
            <div class="muted" style="font-size:13px">继续：${esc(n.course_title)}</div>
        </div>`).join("");

    const reviewHtml = review.length ? review.map((r) => `
        <div class="card pad-sm course-card" onclick="navigate('#/lesson/${r.id}')">
            <div class="cc-head"><div class="cc-icon" style="background:#f59e0b">🔄</div>
            <div><div class="cc-title">${esc(r.title)}</div><div class="muted" style="font-size:12px">上次得分 ${r.score}，建议复习</div></div></div>
        </div>`).join("") : `<div class="empty muted"><div class="e-ico">🎉</div>没有需要复习的课程</div>`;

    shell("首页", `
        <div class="mini-stats">
            <div class="mini-stat"><b>${s.overall_percent}%</b><span>总进度</span></div>
            <div class="mini-stat"><b>${s.completed_lessons}/${s.total_lessons}</b><span>完成课程</span></div>
            <div class="mini-stat"><b>🔥 ${s.streak}</b><span>连续学习</span></div>
            <div class="mini-stat"><b>💎 ${s.points}</b><span>累计积分</span></div>
        </div>
        <div class="section-title">📌 继续学习</div>
        ${next.length ? `<div class="grid grid-3">${nextHtml}</div>` : `<div class="empty"><div class="e-ico">🚀</div>暂无推荐，去课程页开始学习吧！</div>`}
        <div class="spacer"></div>
        <div class="section-title mt2">🔄 待复习</div>
        <div class="grid grid-3">${reviewHtml}</div>
        <div class="spacer"></div>
        <div class="section-title mt2">🌐 学习语言</div>
        <div class="grid grid-3">
            ${["en", "ja", "ko"].map((code) => {
                const ls = prog.languages[code];
                const pct = ls && ls.total ? Math.round(ls.completed * 100 / ls.total) : 0;
                return `<div class="card" onclick="navigate('#/courses?lang=${code}')" style="cursor:pointer">
                    <div style="font-size:32px">${LANG_META[code].flag}</div>
                    <div style="font-weight:800;margin:6px 0">${LANG_META[code].name}</div>
                    <div class="muted" style="font-size:13px">${ls.completed}/${ls.total} 课</div>
                    ${progressBar(ls.completed, ls.total)}
                </div>`;
            }).join("")}
        </div>
    `, "home");
}

/* ================= 课程列表 ================= */
async function viewCourses() {
    const lang = (location.hash.split("?lang=")[1] || "").split("&")[0] || "";
    const [langs, courses] = await Promise.all([api("/languages"), api(lang ? `/courses?language=${lang}` : "/courses")]);
    const all = lang ? courses : courses;
    shell("课程中心", `
        <div class="language-tabs">
            <button class="ltab ${!lang ? "active" : ""}" onclick="navigate('#/courses')">全部</button>
            ${langs.map((l) => `<button class="ltab ${lang === l.code ? "active" : ""}" onclick="navigate('#/courses?lang=${l.code}')">${l.flag} ${l.name}</button>`).join("")}
        </div>
        <div class="grid grid-3">
            ${all.map((c) => `
                <div class="card course-card" onclick="navigate('#/course/${c.id}')">
                    <div class="cc-head">
                        <div class="cc-icon" style="background:${avgColor(c.color)}">${c.icon}</div>
                        <div><div class="cc-title">${esc(c.title)}</div>
                        <span class="level-badge">${esc(c.level)}</span></div>
                    </div>
                    <div class="cc-desc">${esc(c.description)}</div>
                    ${progressBar(c.completed_lessons, c.total_lessons)}
                    <div class="cc-meta"><span>${c.completed_lessons}/${c.total_lessons} 课</span><span>${LANG_META[c.language]?.flag || ""} ${LANG_META[c.language]?.name || ""}</span></div>
                </div>`).join("") || `<div class="empty"><div class="e-ico">📭</div>暂无课程</div>`}
        </div>
    `, "courses");
}

/* ================= 课程详情 ================= */
async function viewCourse(id) {
    const course = await api("/courses/" + id);
    const lessonsHtml = course.lessons.map((l) => {
        const t = TYPE_META[l.type] || {};
        return `
        <div class="card pad-sm ${l.completed ? "" : "course-card"}" onclick="navigate('#/lesson/${l.id}')" style="cursor:pointer">
            <div style="display:flex;align-items:center;gap:12px">
                <div class="cc-icon" style="width:44px;height:44px;font-size:20px;background:${t.color}">${t.icon}</div>
                <div style="flex:1">
                    <div style="font-weight:700">${l.order_index + 1}. ${esc(l.title)}</div>
                    <div class="muted" style="font-size:12.5px">${t.label}</div>
                </div>
                <div style="font-size:22px">${l.completed ? "✅" : "▷"}</div>
            </div>
        </div>`;
    }).join("");
    shell("课程详情", `
        <div class="card" style="margin-bottom:20px">
            <div class="cc-head" style="margin-bottom:8px">
                <div class="cc-icon" style="background:${avgColor(course.color)}">${course.icon}</div>
                <div><div class="cc-title" style="font-size:20px">${esc(course.title)}</div>
                <span class="level-badge">${esc(course.level)}</span></div>
            </div>
            <div class="muted">${esc(course.description)}</div>
            ${progressBar(course.completed_lessons, course.total_lessons)}
            <div class="cc-meta" style="margin-top:10px"><span>已完成 ${course.completed_lessons}/${course.total_lessons} 课</span></div>
        </div>
        <div class="section-title">课程列表</div>
        ${lessonsHtml}
    `, "courses");
}

/* ================= 学习页 ================= */
async function viewLesson(id) {
    const lesson = await api("/lessons/" + id);
    const t = TYPE_META[lesson.type];
    const content = lesson.content || {};
    shell("", `<button class="back" onclick="history.back()">← 返回</button>`, "courses");
    const mainEl = $(".main");
    mainEl.querySelector(".topbar").innerHTML = `
        <div class="lesson-header" style="width:100%">
            <button class="back" onclick="navigate('#/course/${lesson.course_id}')">← ${esc(lesson.course?.title || "返回")}</button>
            <span class="type-badge" style="background:${t.color}22;color:${t.color}">${t.icon} ${t.label}</span>
        </div>`;

    const mount = document.createElement("div");
    mainEl.appendChild(mount);
    mount.id = "lesson-mount";
    mount.lessonId = lesson.id;
    mount.courseId = lesson.course_id;

    if (lesson.type === "vocabulary") renderVocabulary(mount, content, lesson);
    else if (lesson.type === "grammar") renderGrammar(mount, content);
    else if (lesson.type === "speaking") renderSpeaking(mount, content, lesson);
    else if (lesson.type === "listening") renderListening(mount, content, lesson);
}

function lessonDone(score, container) {
    return async () => {
        try {
            const res = await api(`/lessons/${container.lessonId}/complete`, {
                method: "POST", body: JSON.stringify({ score: Math.round(score) }),
            });
            USER = { ...USER, points: res.points, streak: res.streak };
            localStorage.setItem("lingua_user", JSON.stringify(USER));
            const ach = (res.new_achievements || []).map((a) => `🏅 ${a.icon} ${a.name}`).join("<br>");
            container.innerHTML = `<div class="card result-banner">
                <div class="r-num">${Math.round(score)}</div>
                <div class="stars">${"★".repeat(res.stars)}${"☆".repeat(3 - res.stars)}</div>
                <div class="muted">${res.points_gained ? `获得 ${res.points_gained} 积分` : "复习完成，积分已计入"}${ach ? `<div style="margin-top:12px;font-weight:600;color:var(--primary)">🎉 新成就：<br>${ach}</div>` : ""}</div>
                <div style="display:flex;gap:12px;justify-content:center" class="mt2">
                    <button class="btn btn-primary" onclick="navigate('#/course/${container.courseId}')">返回课程</button>
                    <button class="btn btn-ghost" onclick="navigate('#/home')">回到首页</button>
                </div>
            </div>`;
        } catch (e) { toast(e.message); }
    };
}

/* --- 单词记忆 --- */
function renderVocabulary(mount, content, lesson) {
    const words = content.words || [];
    const lang = lesson?.course?.language || "en";
    let idx = 0, flipped = false, known = [];

    function draw() {
        if (idx >= words.length) {
            const score = words.length ? Math.round(known.filter(Boolean).length * 100 / words.length) : 100;
            mount.innerHTML = `<div class="card result-banner">
                <div class="r-num">${score}</div>
                <div class="muted">认识 ${known.filter(Boolean).length}/${words.length} 个单词</div>
                <button class="btn btn-primary mt2" id="finish-btn">完成本课</button>
            </div>`;
            $("#finish-btn").onclick = lessonDone(score, mount);
            return;
        }
        const w = words[idx];
        flipped = false;
        mount.innerHTML = `
            <div class="flashcard-wrap">
                <div class="fc-progress">${idx + 1} / ${words.length}</div>
                <div class="flashcard" id="fc">
                    <div class="fc-word">${flipped ? esc(w.translation) : esc(w.word)}</div>
                    <div class="fc-phonetic">${flipped ? "" : (w.phonetic ? esc(w.phonetic) : "")}</div>
                    <div class="fc-hint">点击卡片翻面查看释义</div>
                </div>
                <div class="fc-controls">
                    <button class="btn btn-ghost" id="btn-unknown">😕 不认识</button>
                    <button class="btn btn-ghost" id="btn-say">🔊</button>
                    <button class="btn btn-primary" id="btn-known">😀 认识</button>
                </div>
            </div>`;
        $("#fc").onclick = () => { flipped = !flipped; draw(); };
        $("#btn-known").onclick = () => { known[idx] = true; idx++; draw(); };
        $("#btn-unknown").onclick = () => { known[idx] = false; idx++; draw(); };
        $("#btn-say").onclick = () => speak(w.word, lang).then(() => {}).catch(() => toast("语音不可用"));
    }
    draw();
}

/* --- 通用选择器（语法 & 听力） --- */
function renderQuiz(mount, { intro = "", points = [], questions = [] }) {
    let stage = questions.length ? "intro" : "done";
    let qi = 0, correct = 0, answered = false;

    function showIntro() {
        mount.innerHTML = `
            <div class="card">
                <div class="muted" style="font-size:15px;margin-bottom:16px">${esc(intro)}</div>
                <div class="point-list">${points.map((p) => `
                    <div class="point-item">
                        <div class="pi-title">${esc(p.title)}</div>
                        <div>${esc(p.explanation)}</div>
                        <div class="ex-box"><span class="ex-t">例句</span><br>${esc(p.example)}<br><span class="muted">${esc(p.example_translation)}</span></div>
                    </div>`).join("")}</div>
                <button class="btn btn-primary mt2" id="start-btn">开始练习</button>
            </div>`;
        $("#start-btn").onclick = () => { stage = "quiz"; showQ(); };
    }

    function showQ() {
        if (qi >= questions.length) { stage = "done"; showResult(); return; }
        const q = questions[qi]; answered = false;
        mount.innerHTML = `<div class="card quiz-q">
            <div class="fc-progress">第 ${qi + 1} / ${questions.length} 题</div>
            <div class="q-text">${esc(q.question)}</div>
            <div class="opts">${q.options.map((o, i) => `<button class="opt" data-i="${i}">${esc(o)}</button>`).join("")}</div>
            <div id="fb" class="quiz-feedback hidden"></div>
            <button class="btn btn-primary mt2 hidden" id="next-btn">下一题</button>
        </div>`;
        mount.querySelectorAll(".opt").forEach((btn) => {
            btn.onclick = () => {
                if (answered) return;
                answered = true;
                const i = +btn.dataset.i;
                const opts = mount.querySelectorAll(".opt");
                opts.forEach((o, k) => {
                    o.disabled = true;
                    if (k === q.answer) o.classList.add("correct");
                    else if (k === i) o.classList.add("wrong");
                });
                if (i === q.answer) correct++;
                const fb = $("#fb");
                fb.classList.remove("hidden");
                fb.innerHTML = (i === q.answer ? "✅ 回答正确！" : "❌ 回答错误") + (q.explanation ? `　<span class="muted">${esc(q.explanation)}</span>` : "");
                const nb = $("#next-btn"); nb.classList.remove("hidden");
                nb.textContent = qi + 1 >= questions.length ? "查看结果" : "下一题";
                nb.onclick = () => { qi++; showQ(); };
            };
        });
    }

    function showResult() {
        const score = questions.length ? Math.round(correct * 100 / questions.length) : 100;
        mount.innerHTML = `<div class="card result-banner">
            <div class="r-num">${score}</div>
            <div class="muted">答对 ${correct}/${questions.length} 题</div>
            <button class="btn btn-primary mt2" id="finish-btn">完成本课</button>
        </div>`;
        $("#finish-btn").onclick = lessonDone(score, mount);
    }

    stage = "intro";
    showIntro();
}

function renderGrammar(mount, content) { renderQuiz(mount, content); }

/* --- 口语跟读 --- */
function renderSpeaking(mount, content, lesson) {
    const sentences = content.sentences || [];
    const lang = lesson.course?.language || "en";
    mount.innerHTML = `
        <div class="card">
            <div class="muted" style="margin-bottom:14px">点击 🔊 听标准发音，点击 🎤 跟读，系统会比对发音相似度。${!speechAvailable() ? "<br><b>提示：</b>当前浏览器不支持语音识别，可点击「已跟读」跳过。" : ""}</div>
            ${sentences.map((s, i) => `
                <div class="speak-item" data-i="${i}">
                    <div style="flex:1">
                        <div class="si-text">${esc(s.text)}</div>
                        <div class="si-meta">${esc(s.phonetic || "")} · ${esc(s.translation)}</div>
                        <div class="sr-result"></div>
                    </div>
                    <button class="icon-btn play-btn" data-i="${i}" title="播放">🔊</button>
                    <button class="icon-btn rec-btn" data-i="${i}" title="跟读">🎤</button>
                    ${!speechAvailable() ? `<button class="btn btn-sm btn-ghost skip-btn" data-i="${i}">已跟读</button>` : ""}
                </div>`).join("")}
            <button class="btn btn-primary btn-block mt2" id="speak-done">完成本课</button>
        </div>`;

    const results = new Array(sentences.length).fill(null);
    function setResult(i, html) { mount.querySelector(`.speak-item[data-i="${i}"] .sr-result`).innerHTML = html; }

    mount.querySelectorAll(".play-btn").forEach((b) => {
        b.onclick = async () => { try { await speak(sentences[+b.dataset.i].text, lang); } catch { toast("语音合成不可用"); } };
    });
    mount.querySelectorAll(".rec-btn").forEach((b) => {
        b.onclick = async () => {
            const i = +b.dataset.i, btn = b;
            btn.classList.add("rec"); setResult(i, "🎧 请跟读…");
            try {
                const transcript = await recognize(lang);
                const sim = similarity(transcript, sentences[i].text);
                results[i] = sim;
                setResult(i, `识别：${esc(transcript) || "（未识别）"}　<span class="match-pill" style="color:${sim >= 70 ? "var(--success)" : sim >= 40 ? "var(--warning)" : "var(--danger)"}">${sim}% 相似</span>`);
            } catch (e) {
                setResult(i, `<span class="muted">${esc(e.message)}</span>`);
            } finally { btn.classList.remove("rec"); }
        };
    });
    mount.querySelectorAll(".skip-btn").forEach((b) => {
        b.onclick = () => { const i = +b.dataset.i; results[i] = 100; setResult(i, "✅ 已跟读"); };
    });

    $("#speak-done").onclick = () => {
        const scored = results.filter((r) => r !== null);
        const avg = scored.length ? scored.reduce((a, b) => a + b, 0) / scored.length : 100;
        lessonDone(avg, mount)();
    };
}

/* --- 听力训练 --- */
function renderListening(mount, content, lesson) {
    const lang = lesson.course?.language || "en";
    const q = content.questions || [];
    mount.innerHTML = `
        <div class="card" style="margin-bottom:16px">
            <div class="cc-head">
                <div class="cc-icon" style="background:#14b8a6">🎧</div>
                <div><div style="font-weight:800">听录音回答问题</div><div class="muted" style="font-size:13px">可多次播放</div></div>
            </div>
            <div style="display:flex;gap:10px;margin-top:12px">
                <button class="btn btn-primary" id="play-audio">▶️ 播放听力</button>
                <button class="btn btn-ghost" id="toggle-tran">显示原文</button>
            </div>
            <div class="quiz-feedback mt" id="audio-text" style="display:none">${esc(content.audio_text)}<div class="muted" style="font-size:13px">${esc(content.translation)}</div></div>
        </div>
        <div id="listen-quiz"></div>`;

    $("#play-audio").onclick = async () => {
        try { await speak(content.audio_text, lang); } catch { toast("语音合成不可用"); }
    };
    $("#toggle-tran").onclick = () => { const el = $("#audio-text"); el.style.display = el.style.display === "none" ? "block" : "none"; };

    const quizEl = $("#listen-quiz");
    quizEl.lessonId = mount.lessonId;
    quizEl.courseId = mount.courseId;
    renderQuiz(quizEl, { intro: "", points: [], questions: q });
}

/* ================= 学习进度 ================= */
async function viewProgress() {
    const prog = await api("/progress");
    const s = prog.stats;
    shell("学习进度", `
        <div class="grid grid-3" style="margin-bottom:20px">
            <div class="card" style="text-align:center">
                <div class="ring" style="--p:${s.overall_percent}"><div class="pct">${s.overall_percent}%</div></div>
                <div class="muted">总体完成度</div>
            </div>
            <div class="card">
                <h3>📊 学习统计</h3>
                <div class="mini-stats" style="grid-template-columns:repeat(2,1fr)">
                    <div class="mini-stat"><b>${s.completed_lessons}</b><span>完成课程</span></div>
                    <div class="mini-stat"><b>${s.total_lessons}</b><span>全部课程</span></div>
                    <div class="mini-stat"><b>${s.completed_today}</b><span>今日完成</span></div>
                    <div class="mini-stat"><b>🔥 ${s.streak}</b><span>连续天数</span></div>
                </div>
            </div>
            <div class="card">
                <h3>💎 积分</h3>
                <div style="font-size:44px;font-weight:800;color:var(--primary)">${s.points}</div>
                <div class="muted">累计学习积分</div>
            </div>
        </div>
        <div class="card">
            <h3>🌐 各语言进度</h3>
            ${["en", "ja", "ko"].map((code) => {
                const ls = prog.languages[code];
                const pct = ls && ls.total ? Math.round(ls.completed * 100 / ls.total) : 0;
                return `<div class="lang-bar">
                    <div class="lb-name">${LANG_META[code].flag} ${LANG_META[code].name}</div>
                    <div class="lb-track"><div style="width:${pct}%"></div></div>
                    <div class="lb-pct">${pct}%</div>
                </div>`;
            }).join("")}
        </div>
        <div class="card mt2">
            <h3>📚 课程明细</h3>
            ${prog.courses.map((c) => `
                <div class="lang-bar">
                    <div class="lb-name">${c.icon} ${esc(c.title)}</div>
                    <div class="lb-track"><div style="width:${c.done ? Math.round(c.done * 100 / 4) : 0}%"></div></div>
                    <div class="lb-pct">${c.done}/4</div>
                </div>`).join("")}
        </div>
    `, "progress");
}

/* ================= 社区 ================= */
async function viewCommunity() {
    const data = await api("/posts");
    const langs = ["all", "en", "ja", "ko"];
    shell("学习社区", `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
            <div class="language-tabs" style="margin-bottom:0">
                ${langs.map((l) => `<button class="ltab ${l === "all" ? "active" : ""}" data-lang="${l}">${l === "all" ? "综合" : LANG_META[l].flag + " " + LANG_META[l].name}</button>`).join("")}
            </div>
            <button class="btn btn-primary" id="new-post">✍️ 发帖</button>
        </div>
        <div id="post-list" class="grid" style="grid-template-columns:1fr">
            ${renderPostList(data.posts)}
        </div>`);

    document.querySelectorAll(".language-tabs .ltab").forEach((b) => {
        b.onclick = async () => {
            document.querySelectorAll(".language-tabs .ltab").forEach((x) => x.classList.remove("active"));
            b.classList.add("active");
            const lang = b.dataset.lang;
            const res = await api(lang === "all" ? "/posts" : "/posts?language=" + lang);
            $("#post-list").innerHTML = renderPostList(res.posts);
            bindPostCards();
        };
    });
    $("#new-post").onclick = () => showPostEditor();
    bindPostCards();
}

function renderPostList(posts) {
    if (!posts.length) return `<div class="empty" style="grid-column:1"><div class="e-ico">💬</div>还没有帖子，快来发第一帖吧</div>`;
    return posts.map((p) => `
        <div class="card post-card" data-id="${p.id}">
            <div class="pc-top">
                <div class="avatar" style="width:34px;height:34px;font-size:14px">${esc(p.author[0].toUpperCase())}</div>
                <span class="pc-author">${esc(p.author)}</span>
                <span class="tag">${esc(p.language_name)}</span>
                <span class="pc-time">${fmtTime(p.created_at)}</span>
            </div>
            <h3>${esc(p.title)}</h3>
            <div class="pc-body">${esc(p.content)}</div>
            <div class="pc-actions">
                <span class="like-btn" data-id="${p.id}" style="cursor:pointer;color:${p.liked ? "var(--danger)" : "inherit"}">❤️ ${p.like_count}</span>
                <span>💬 ${p.comment_count}</span>
            </div>
        </div>`).join("");
}

function bindPostCards() {
    document.querySelectorAll(".post-card").forEach((c) => {
        c.onclick = (e) => { if (!e.target.closest(".like-btn")) navigate("#/post/" + c.dataset.id); };
    });
    document.querySelectorAll(".like-btn").forEach((b) => {
        b.onclick = async (e) => {
            e.stopPropagation();
            const res = await api(`/posts/${b.dataset.id}/like`, { method: "POST" });
            b.style.color = res.liked ? "var(--danger)" : "inherit";
            b.innerHTML = `❤️ ${res.like_count}`;
        };
    });
}

function showPostEditor() {
    const backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.innerHTML = `<div class="modal">
        <h3>发布新帖</h3>
        <div class="field"><label>标题</label><input id="p-title" maxlength="80" placeholder="例如：日语五十音学习心得" /></div>
        <div class="field"><label>内容</label><textarea id="p-content" maxlength="3000" placeholder="分享你的学习经验、问题或资源…"></textarea></div>
        <div class="field"><label>关联语言</label>
            <div class="chip-group" id="p-lang">
                <button type="button" class="chip active" data-lang="all">综合</button>
                <button type="button" class="chip" data-lang="en">英语</button>
                <button type="button" class="chip" data-lang="ja">日语</button>
                <button type="button" class="chip" data-lang="ko">韩语</button>
            </div>
        </div>
        <div style="display:flex;gap:12px;justify-content:flex-end;margin-top:20px">
            <button class="btn btn-ghost" id="p-cancel">取消</button>
            <button class="btn btn-primary" id="p-submit">发布</button>
        </div>
    </div>`;
    document.body.appendChild(backdrop);
    backdrop.querySelectorAll("#p-lang .chip").forEach((c) => c.onclick = () => {
        backdrop.querySelectorAll("#p-lang .chip").forEach((x) => x.classList.remove("active"));
        c.classList.add("active");
    });
    $("#p-cancel").onclick = () => backdrop.remove();
    backdrop.onclick = (e) => { if (e.target === backdrop) backdrop.remove(); };
    $("#p-submit").onclick = async () => {
        const lang = backdrop.querySelector("#p-lang .chip.active").dataset.lang;
        const payload = { title: $("#p-title").value.trim(), content: $("#p-content").value.trim(), language: lang };
        if (!payload.title || !payload.content) return toast("标题与内容不能为空");
        try {
            const res = await api("/posts", { method: "POST", body: JSON.stringify(payload) });
            backdrop.remove();
            toast(res.new_achievements?.length ? "发布成功，解锁新成就！" : "发布成功");
            viewCommunity();
        } catch (e) { toast(e.message); }
    };
}

/* ================= 帖子详情 ================= */
async function viewPost(id) {
    const p = await api("/posts/" + id);
    const comments = (p.comments || []).map((c) => `
        <div class="comment">
            <div class="avatar">${esc(c.author[0].toUpperCase())}</div>
            <div class="c-body"><div class="c-author">${esc(c.author)}</div><div class="c-text">${esc(c.content)}</div></div>
        </div>`).join("");
    shell("帖子详情", `
        <button class="back" onclick="history.back()" style="margin-bottom:14px;display:inline-flex;align-items:center;gap:6px;color:var(--text-2);font-weight:600">← 返回社区</button>
        <div class="card">
            <div class="pc-top">
                <div class="avatar">${esc(p.author[0].toUpperCase())}</div><span class="pc-author">${esc(p.author)}</span>
                <span class="tag">${esc(p.language_name)}</span><span class="pc-time">${fmtTime(p.created_at)}</span>
            </div>
            <h3 style="margin:8px 0">${esc(p.title)}</h3>
            <div style="white-space:pre-wrap">${esc(p.content)}</div>
            <div class="pc-actions" style="margin-top:16px">
                <span class="like-btn" data-id="${p.id}" style="cursor:pointer;color:${p.liked ? "var(--danger)" : "inherit"}">❤️ ${p.like_count}</span>
                <span>💬 ${p.comment_count} 条评论</span>
            </div>
        </div>
        <div class="card mt2">
            <h3>评论</h3>
            ${comments || `<div class="muted">暂无评论</div>`}
            <div class="field mt2" style="display:flex;gap:10px;align-items:center">
                <input id="c-input" placeholder="写下你的评论…" style="flex:1" />
                <button class="btn btn-primary" id="c-send">发送</button>
            </div>
        </div>`);
    document.querySelector(".like-btn").onclick = async (e) => {
        const res = await api(`/posts/${p.id}/like`, { method: "POST" });
        const btn = document.querySelector(".like-btn");
        btn.style.color = res.liked ? "var(--danger)" : "inherit";
        btn.innerHTML = `❤️ ${res.like_count}`;
    };
    $("#c-send").onclick = async () => {
        const content = $("#c-input").value.trim();
        if (!content) return toast("评论不能为空");
        try { await api(`/posts/${p.id}/comments`, { method: "POST", body: JSON.stringify({ content }) }); viewPost(id); }
        catch (e) { toast(e.message); }
    };
}

/* ================= 成就 ================= */
async function viewAchievements() {
    const data = await api("/achievements");
    shell("成就系统", `
        <div class="card" style="margin-bottom:18px;display:flex;align-items:center;gap:16px">
            <div style="font-size:42px">🏆</div>
            <div><div style="font-weight:800;font-size:18px">已解锁 ${data.unlocked_count} / ${data.achievements.length} 个成就</div>
            <div class="muted">坚持学习，解锁更多成就！</div></div>
        </div>
        <div class="ach-grid">
            ${data.achievements.map((a) => `
                <div class="ach-card ${a.unlocked ? "" : "locked"}">
                    <div class="a-icon">${a.icon}</div>
                    <div class="a-name">${esc(a.name)}</div>
                    <div class="a-desc">${esc(a.description)}</div>
                    <div class="muted" style="font-size:11px;margin-top:6px">${a.unlocked ? "✅ 已解锁" : "🔒 未解锁"}</div>
                </div>`).join("")}
        </div>
    `, "achievements");
}

/* ================= 设置 ================= */
async function viewProfile() {
    const langs = await api("/languages");
    const targets = USER?.target_languages || ["en"];
    shell("个人设置", `
        <div class="card" style="max-width:520px">
            <h3>学习偏好</h3>
            <div class="field">
                <label>母语</label>
                <select id="pf-native">
                    <option value="zh" ${USER?.native_language === "zh" ? "selected" : ""}>中文</option>
                    <option value="en" ${USER?.native_language === "en" ? "selected" : ""}>English</option>
                    <option value="ja" ${USER?.native_language === "ja" ? "selected" : ""}>日本語</option>
                    <option value="ko" ${USER?.native_language === "ko" ? "selected" : ""}>한국어</option>
                </select>
            </div>
            <div class="field">
                <label>目标语言</label>
                <div class="chip-group" id="pf-langs">
                    ${langs.map((l) => `<button type="button" class="chip ${targets.includes(l.code) ? "active" : ""}" data-lang="${l.code}">${l.flag} ${l.name}</button>`).join("")}
                </div>
            </div>
            <div class="field">
                <label>当前水平</label>
                <select id="pf-level">
                    ${["A1", "A2", "B1", "B2"].map((lv) => `<option value="${lv}" ${USER?.level === lv ? "selected" : ""}>${lv}</option>`).join("")}
                </select>
            </div>
            <button class="btn btn-primary" id="pf-save">保存设置</button>
            <button class="btn btn-ghost" id="pf-logout" style="margin-left:8px">退出登录</button>
        </div>`);
    document.querySelectorAll("#pf-langs .chip").forEach((c) => c.onclick = () => c.classList.toggle("active"));
    $("#pf-save").onclick = async () => {
        const pay = {
            native_language: $("#pf-native").value,
            level: $("#pf-level").value,
            target_languages: [...document.querySelectorAll("#pf-langs .chip.active")].map((c) => c.dataset.lang),
        };
        try {
            USER = await api("/auth/profile", { method: "PUT", body: JSON.stringify(pay) });
            localStorage.setItem("lingua_user", JSON.stringify(USER));
            toast("设置已保存");
            navigate("#/home");
        } catch (e) { toast(e.message); }
    };
    $("#pf-logout").onclick = async () => {
        try { await api("/auth/logout", { method: "POST" }); } catch {}
        clearAuth();
        toast("已退出登录");
        navigate("#/login");
    };
}

/* ================= 启动 ================= */
if (!location.hash) location.hash = "#/home";
render();