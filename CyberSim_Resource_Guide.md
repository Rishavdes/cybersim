# 📚 CyberSim Complete Resource Guide
> **How to add resources, what's already done, and the roadmap to 100% coverage.**

---

## Table of Contents
1. [What's Already Built](#1-whats-already-built)
2. [How to Add New Resources (Step-by-Step)](#2-how-to-add-new-resources)
3. [What to Add for 100% Coverage](#3-what-to-add-for-100-coverage)
4. [Future Addon Ideas](#4-future-addon-ideas)

---

## 1. What's Already Built

### 📁 Files You Can Edit (No Code Changes Needed)

| File | What It Stores | How It's Used |
|------|---------------|---------------|
| `db/academy_courses.json` | Videos, PDFs, Labs for each academy topic | Shown in `[11] Learning Academy` menu |
| `db/reward_courses.json` | Exclusive course download links (XP rewards) | Shown when user buys a reward in `[7] Reward Shop` |

### 📊 Current Content Summary

| Component | Count | Details |
|-----------|-------|---------|
| Daily missions | 74 | Across 730 days (2 years) |
| Docker labs | 13 | Real vulnerable targets |
| OWASP modules | 10 | Full OWASP Top 10 interactive training |
| Academy topics | 16 | Beginner(4) + Intermediate(5) + Advanced(7) |
| Exclusive courses | 10 | 50+ elhacker download links |
| Reward shop items | 28 | Titles, themes, resources, courses |

### 📦 What's Already Added Per Topic

| Topic | Missions | elhacker Videos | Labs | PDFs | Academy Status |
|-------|----------|----------------|------|------|----------------|
| Networking | 9 | ✅ 1 course | ✅ 3 | ⬜ PLACEHOLDER | ✅ In Beginner |
| Linux | 8 | ✅ 3 courses | ✅ 3 | ⬜ PLACEHOLDER | ✅ In Beginner |
| Python | 7 | ✅ 2 courses | ✅ 2 | ⬜ 1 free link + 1 PLACEHOLDER | ✅ In Beginner |
| Security+ | 3 | ✅ 2 courses | ⬜ None | ⬜ PLACEHOLDER | ✅ In Beginner |
| Privilege Escalation | 7 | ✅ 2 courses | ✅ 2 | ⬜ 1 free link + 1 PLACEHOLDER | ✅ In Intermediate |
| Cryptography | 7 | ⬜ PLACEHOLDER | ✅ 2 | ⬜ PLACEHOLDER | ✅ In Intermediate |
| Web Hacking | 6 | ✅ 3 courses | ✅ 3 | ⬜ PLACEHOLDER | ✅ In Intermediate |
| CEH Prep | — | ✅ 4 courses | ⬜ None | ⬜ PLACEHOLDER | ✅ In Intermediate |
| CTF Practice | 6 | ⬜ PLACEHOLDER | ✅ 3 | ⬜ PLACEHOLDER | ✅ In Intermediate |
| Active Directory | 2 | ✅ 3 courses | ✅ 2 | ⬜ PLACEHOLDER | ✅ In Advanced |
| Buffer Overflow | 2 | ✅ 3 courses | ✅ 2 | ⬜ PLACEHOLDER | ✅ In Advanced |
| Blue Team/SOC | 3 | ✅ 1 course | ✅ 1 | ⬜ PLACEHOLDER | ✅ In Advanced |
| Malware Dev | 2 | ✅ 4 courses | ✅ 1 | ⬜ PLACEHOLDER | ✅ In Advanced |
| Red Team/C2 | 3 | ✅ 4 courses | ⬜ None | ⬜ PLACEHOLDER | ✅ In Advanced |
| WiFi & Cloud | 2 | ✅ 3 courses | ✅ 2 | ⬜ PLACEHOLDER | ✅ In Advanced |
| Career | 7 | ⬜ PLACEHOLDER | ✅ 2 | ⬜ PLACEHOLDER | ✅ In Advanced |

> ⬜ PLACEHOLDER = entry exists in JSON, you just need to replace the URL

---

## 2. How to Add New Resources

### Step 1: Open the Data File

```bash
# For academy learning resources:
nano /home/hacker/Desktop/python\ learning\ \ and\ hacking\ \ simulation/cybersim/db/academy_courses.json

# For exclusive reward course links:
nano /home/hacker/Desktop/python\ learning\ \ and\ hacking\ \ simulation/cybersim/db/reward_courses.json
```

Or open in VS Code / any text editor.

---

### Step 2: Find the Topic You Want to Update

The `academy_courses.json` structure:
```
{
  "beginner" → topics → "Networking Fundamentals" → videos / pdfs / labs
  "intermediate" → topics → "Web Application Hacking" → videos / pdfs / labs
  "advanced" → topics → "Active Directory" → videos / pdfs / labs
}
```

---

### Step 3: Add a Video Lecture

Find the topic and add to the `"videos"` array:
```json
"videos": [
    {"name": "Existing Course", "url": "https://existing-link", "platform": "elhacker"},
    {"name": "YOUR NEW COURSE NAME", "url": "YOUR_LINK_HERE", "platform": "telegram"}
]
```

**Platform options:**
| Platform | Value | When to Use |
|----------|-------|-------------|
| Telegram | `"telegram"` | Telegram channel links |
| Google Drive | `"gdrive"` | Google Drive shared folders |
| elhacker.INFO | `"elhacker"` | ns2.elhacker.info links |
| YouTube | `"youtube"` | YouTube playlists/videos |
| Web | `"web"` | Any website URL |

---

### Step 4: Add a PDF

Find the topic and add to the `"pdfs"` array:
```json
"pdfs": [
    {"name": "YOUR PDF NAME", "url": "https://your-google-drive-or-telegram-link", "platform": "gdrive"}
]
```

---

### Step 5: Add a Lab

Find the topic and add to the `"labs"` array:
```json
"labs": [
    {"name": "Lab Name", "url": "https://tryhackme.com/room/example", "platform": "web"},
    {"name": "Docker Lab", "url": "docker:your_lab_name", "platform": "lab"}
]
```

---

### Step 6: Replace a PLACEHOLDER

Search for `"PLACEHOLDER"` in the JSON and replace with real URLs:
```diff
- {"name": "CompTIA Network+ Study Guide PDF", "url": "PLACEHOLDER", "platform": "gdrive"}
+ {"name": "CompTIA Network+ Study Guide PDF", "url": "https://drive.google.com/your-link", "platform": "gdrive"}
```

---

### Step 7: Add a New Exclusive Reward Course

Edit `db/reward_courses.json`:
```json
{
  "your_course_id": {
    "title": "Course Display Name",
    "links": [
      {"name": "Part 1", "url": "https://link1", "platform": "elhacker"},
      {"name": "Part 2", "url": "https://link2", "platform": "telegram"}
    ]
  }
}
```

Then also add the reward to `core/rewards.py` in the `REWARDS` list:
```python
{"id": "your_course_id", "cost": 5000, "type": "course",
 "name": "💀 Your Course (EXCLUSIVE)",
 "desc": "Description here."},
```

---

### Step 8: Verify Your Changes

```bash
cd /home/hacker/Desktop/python\ learning\ \ and\ hacking\ \ simulation/cybersim

# Check JSON is valid:
python3 -c "import json; json.load(open('db/academy_courses.json')); print('✅ Academy JSON OK')"
python3 -c "import json; json.load(open('db/reward_courses.json')); print('✅ Rewards JSON OK')"

# Run the app and test:
python3 gamemaster.py
# → Choose [11] → Learning Academy to see your changes
```

---

## 3. What to Add for 100% Coverage

### 🔴 Priority 1: Topics at 40-50% (Need Most Work)

#### Red Team/C2 (40% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Red Team & C2 Operations`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | PNPT Full Course | `https://ns2.elhacker.info/descargas/TCM%20-%20Practical%20Network%20Penetration%20Tester%20(PNPT)/` | elhacker |
| 📹 Video | Throwback AD Network THM | `https://tryhackme.com/network/throwback` | web |
| 📹 Video | C2 Matrix Overview | `https://www.thec2matrix.com/` | web |
| 📄 PDF | Red Team Field Manual | Add your Telegram/GDrive link | telegram |
| 🧪 Lab | THM - Wreath Network | `https://tryhackme.com/room/wreath` | web |
| 🧪 Lab | THM - Holo Live Network | `https://tryhackme.com/room/hololive` | web |

---

#### Blue Team/SOC/DFIR (45% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Blue Team & SOC`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | Blue Team Level 1 | `https://ns2.elhacker.info/descargas/Blue%20Team%20Level%201/` | elhacker |
| 📹 Video | SANS SEC504 Hacker Tools | `https://ns2.elhacker.info/descargas/SEC504/` | elhacker |
| 📹 Video | TCM Security Operations | Add your Telegram link | telegram |
| 📄 PDF | SANS DFIR Poster | `https://www.sans.org/posters/` (free) | web |
| 🧪 Lab | LetsDefend.io | `https://app.letsdefend.io/` (free tier) | web |
| 🧪 Lab | CyberDefenders.org | `https://cyberdefenders.org/blueteamctf/` | web |
| 🧪 Lab | Splunk BOTS v1 | `https://github.com/splunk/botsv1` | web |

---

#### Malware Dev (50% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Malware Development`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | Sektor7 Malware Dev Advanced | `https://ns2.elhacker.info/descargas/Sektor7%20Malware%20Development%20Advanced/` | elhacker |
| 📹 Video | Practical Malware Analysis & Triage | `https://ns2.elhacker.info/descargas/Practical%20Malware%20Analysis%20and%20Triage/` | elhacker |
| 📹 Video | SANS SEC699 Purple Team | `https://ns2.elhacker.info/descargas/SEC699/` | elhacker |
| 📄 PDF | ired.team Red Team Notes | `https://www.ired.team/` | web |
| 🧪 Lab | MalwareBazaar Samples | `https://bazaar.abuse.ch/` | web |

---

#### WiFi & Cloud (50% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Wireless & Cloud Hacking`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | Attacking & Defending AWS | `https://ns2.elhacker.info/descargas/Attacking%20and%20Defending%20AWS/` | elhacker |
| 📹 Video | WiFi Hacking with Aircrack-ng | Add your Telegram link | telegram |
| 📄 PDF | WiFi Pentesting Cheatsheet | Add your GDrive link | gdrive |
| 🧪 Lab | CloudGoat (AWS) | `https://github.com/RhinoSecurityLabs/cloudgoat` | web |
| 🧪 Lab | flAWS Cloud CTF | `http://flaws.cloud/` | web |
| 🧪 Lab | flAWS2 Cloud CTF | `http://flaws2.cloud/` | web |

---

### 🟡 Priority 2: Topics at 55-60%

#### Active Directory (55% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Active Directory`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | CRTP Certified Red Team Pro | `https://ns2.elhacker.info/descargas/Certified%20Red%20Team%20Professional%20(CRTP)/` | elhacker |
| 📹 Video | OffSec OSEP (PEN-300) | `https://ns2.elhacker.info/descargas/OSEP/` | elhacker |
| 📹 Video | AD Purple Team Lab Build | `https://ns2.elhacker.info/descargas/Active%20Directory%20Purple%20Team%20Lab/` | elhacker |
| 🧪 Lab | THM - Active Directory Basics | `https://tryhackme.com/room/winadbasics` | web |
| 🧪 Lab | THM - Attacktive Directory | `https://tryhackme.com/room/attacktivedirectory` | web |
| 🧪 Lab | DVAD (Damn Vulnerable AD) | `https://github.com/WazeHell/vulnerable-AD` | web |

---

#### Buffer Overflow (60% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Buffer Overflow & Exploit Dev`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | OSED Prep (Windows Exploit Dev) | `https://ns2.elhacker.info/descargas/OSED/` | elhacker |
| 📹 Video | Heap Exploitation Course | Add your Telegram link | telegram |
| 📄 PDF | ROP Emporium Guide | `https://ropemporium.com/` | web |
| 🧪 Lab | ROP Emporium Challenges | `https://ropemporium.com/` | web |
| 🧪 Lab | pwnable.kr | `https://pwnable.kr/` | web |

---

#### Security+ Theory (60% → 100%)

**Add to:** `db/academy_courses.json` → `beginner` → `Security Concepts`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | Professor Messer Security+ (FREE) | `https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/sy0-701-comptia-security-702-course/` | youtube |
| 📹 Video | CompTIA Security+ SY0-701 | Add your Telegram link | telegram |
| 📄 PDF | NIST Cybersecurity Framework | `https://www.nist.gov/cyberframework` | web |
| 📄 PDF | Security+ Exam Objectives | `https://www.comptia.org/certifications/security` | web |
| 🧪 Lab | TryHackMe - Security Engineer | `https://tryhackme.com/path/outline/security-engineer-training` | web |

---

### 🟢 Priority 3: Topics at 70-75% (Quick Fixes)

#### Python for Hacking (75% → 100%)

**Add to:** `db/academy_courses.json` → `beginner` → `Python for Hacking`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | Black Hat Python Book Course | Add your Telegram link | telegram |
| 📄 PDF | Black Hat Python 2e PDF | Add your GDrive link | gdrive |
| 🧪 Lab | TryHackMe - Python for Pentesters | `https://tryhackme.com/room/pythonforcybersecurity` | web |

---

#### CTF Practice (70% → 100%)

**Add to:** `db/academy_courses.json` → `intermediate` → `CTF Practice`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | IppSec HTB Walkthroughs | `https://www.youtube.com/@ippsec` | youtube |
| 📹 Video | John Hammond CTFs | `https://www.youtube.com/@_JohnHammond` | youtube |
| 🧪 Lab | VulnHub | `https://vulnhub.com/` | web |
| 🧪 Lab | Hack The Box Academy | `https://academy.hackthebox.com/` | web |

---

#### Career & Bug Bounty (70% → 100%)

**Add to:** `db/academy_courses.json` → `advanced` → `Certification & Career`

| Type | Name | URL | Platform |
|------|------|-----|----------|
| 📹 Video | Bug Bounty Bootcamp | `https://ns2.elhacker.info/descargas/Bug%20Bounty%20Bootcamp/` | elhacker |
| 📹 Video | OSCP Complete Prep | Add your Telegram link | telegram |
| 📄 PDF | OSCP Exam Preparation Guide | Add your GDrive link | gdrive |
| 🧪 Lab | HackerOne Programs | `https://hackerone.com/directory/programs` | web |

---

## 4. Future Addon Ideas

### 🆕 New Topics to Add (Currently 0% — Not in App Yet)

These topics would make CyberSim truly complete. Add them as **new topics** in `db/academy_courses.json`:

#### How to Add a New Topic

1. Open `db/academy_courses.json`
2. Find the right level (`beginner`, `intermediate`, or `advanced`)
3. Add inside `"topics"`:
```json
"Your New Topic Name": {
    "mission_ids": [],
    "description": "What this topic covers",
    "videos": [
        {"name": "Course Name", "url": "https://link", "platform": "elhacker"}
    ],
    "pdfs": [
        {"name": "PDF Name", "url": "https://link", "platform": "gdrive"}
    ],
    "labs": [
        {"name": "Lab Name", "url": "https://link", "platform": "web"}
    ]
}
```

> **Note:** `mission_ids` can be empty `[]` — the topic will still show up with its resources, just without playable missions.

---

#### Suggested New Topics

| Topic | Level | elhacker.INFO Courses Available |
|-------|-------|-------------------------------|
| **OSINT & Recon** | Intermediate | `TCM - OSINT Fundamentals/` (already in reward shop) |
| **Android/Mobile Hacking** | Advanced | `Android App Hacking Black Belt/` (already in reward shop) |
| **Reverse Engineering** | Advanced | `Reverse Engineering Ghidra/IDA/` (already in reward shop) |
| **Hardware Hacking** | Advanced | `Flipper Zero Course/` (already in reward shop) |
| **Dark Web & Anonymity** | Advanced | `Ultimate Dark Web Course/` (already in reward shop) |
| **Physical Security & SE** | Advanced | `Physical Red Teaming/` (already in reward shop) |
| **Docker & Kubernetes Security** | Advanced | Search elhacker for container security |
| **API Pentesting** | Intermediate | `APIsec University/` (free: apisecuniversity.com) |
| **Blockchain Security** | Advanced | Search elhacker for smart contract hacking |
| **AI/ML Security** | Advanced | Adversarial ML, prompt injection |

---

### 🔧 Future Code Enhancements

| Enhancement | Where to Add | Difficulty |
|-------------|-------------|------------|
| **Academy progress tracking** | Save viewed topics to `db/state.json` in `academy.py` | Easy |
| **XP for academy study** | Award 25 XP per topic viewed in `academy.py` | Easy |
| **Search across all courses** | Add search function to `academy.py` | Medium |
| **Auto-download from Telegram** | New module `core/telegram_downloader.py` | Hard |
| **Google Drive integration** | New module `core/gdrive_sync.py` | Hard |
| **Course completion certificates** | Generate PDF certificates in `rewards.py` | Medium |
| **Peer study groups** | Discord/Telegram group links per topic | Easy |
| **Weekly challenges** | Timed CTF challenges with bonus XP | Medium |

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────┐
│              CYBERSIM FILE LOCATIONS                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  📁 db/academy_courses.json                          │
│     → All learning resources (videos/pdfs/labs)      │
│     → Edit this to add new course links              │
│                                                      │
│  📁 db/reward_courses.json                           │
│     → Exclusive reward shop course links             │
│     → Edit this to add download URLs                 │
│                                                      │
│  📁 core/academy.py                                  │
│     → Learning Academy code (don't edit unless       │
│       adding new features)                           │
│                                                      │
│  📁 core/rewards.py → REWARDS list                   │
│     → Add new reward items here                      │
│                                                      │
│  📁 db/state.json                                    │
│     → User progress data (auto-managed)              │
│                                                      │
│  🔍 audit_missions.py                                │
│     → Run to check mission completeness              │
│                                                      │
└──────────────────────────────────────────────────────┘

Validate JSON after editing:
  python3 -c "import json; json.load(open('db/academy_courses.json')); print('OK')"

Run the app:
  python3 gamemaster.py → [11] Learning Academy
```
