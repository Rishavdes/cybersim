# 🚀 Step-by-Step Guide: Uploading CyberSim to GitHub

Congratulations on building CyberSim v2.0! This is a massive, highly impressive project (77 missions, AI integration, 3 difficulty tiers) that will look amazing on your resume and portfolio.

Here is exactly how to upload it to your GitHub profile so employers, recruiters, and the community can see it.

---

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in to your account.
2. In the top-right corner, click the **`+`** icon and select **New repository**.
3. **Repository name**: `cybersim`
4. **Description**: `AI-powered, local cybersecurity training range with 77 missions and active AI defense.`
5. **Visibility**: Select **Public** so employers and the community can see your work.
6. **Initialize this repository**: 
   - ⚠️ Do **NOT** check "Add a README file" (we already created a great one for you!).
   - ⚠️ Do **NOT** add a `.gitignore` or `license` right now.
7. Click the green **Create repository** button.

---

## Step 2: Push Your Local Code to GitHub

Open your Kali Linux terminal, navigate to your project folder, and run these commands one by one.

### 1. Navigate to the project folder
```bash
cd "/home/hacker/Desktop/python learning  and hacking  simulation/cybersim"
```

### 2. Initialize Git (if you haven't already)
```bash
git init
```

### 3. Add all your files
This stages all your code, the new README, and the Docker targets to be uploaded.
```bash
git add .
```

### 4. Commit your files
This saves a "snapshot" of your code.
```bash
git commit -m "Initial commit: CyberSim v2.0 complete release featuring 77 missions, AI mentor, and difficulty scaling"
```

### 5. Link to your new GitHub repository
*Note: Replace `YOUR_USERNAME` with your actual GitHub username.*
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cybersim.git
```

### 6. Push the code online!
```bash
git push -u origin main
```
*(GitHub will ask for your username and password. For the password, you must use a **Personal Access Token**. See troubleshooting below if you don't have one).*

---

## Step 3: Best Practices & Polishing

Now that your code is on GitHub, let's make the repository look extremely professional for recruiters.

### Add Tags (Topics)
On your repository's main page on GitHub, look strictly to the right under "About". Click the gear icon ⚙️ and add these tags:
`cybersecurity` `python` `ai` `red-team` `blue-team` `docker` `simulator` `infosec` `kali-linux`

### Pin to Profile
Go to your main GitHub profile page (`github.com/YOUR_USERNAME`).
Under "Pinned", click "Customize your pins" and select **cybersim**. This ensures it's the very first thing anyone sees when they visit your profile!

---

## 🛑 Troubleshooting: "Authentication Failed"

If you get an error when running `git push` that says password authentication was removed:
1. Go to GitHub Settings → Developer Settings → [Personal access tokens (Tokens (classic))](https://github.com/settings/tokens).
2. Click **Generate new token (classic)**.
3. Note: `CyberSim Upload`, Expiration: `30 days` (or No expiration).
4. Check the box for **`repo`** (Full control of private repositories).
5. Scroll down to click **Generate token**.
6. **COPY THE TOKEN** (it looks like `ghp_xxxxxxxxxxxxxxxxx`).
7. Go back to your terminal, run `git push -u origin main` again. Use your username, and paste the token as your password.
