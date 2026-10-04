# Cheed Home Care website

Plain HTML/CSS/JS site for **cheedhomecare.com**, hosted free on GitHub Pages.

```
index.html       Home
about.html       About us
services.html    Services
contact.html     Contact form
resources.html   Resources for seniors in Alberta (the "free guide")
404.html         Page-not-found
css/styles.css   All styling
js/main.js       Mobile menu + contact form
images/          Your photos go here (see images/README.txt)
CNAME            Tells GitHub Pages to use cheedhomecare.com
```

## 1. Connect the contact form (free, 5 minutes)

1. Go to **web3forms.com**, enter the email that should receive enquiries (e.g. info@cheedinc.com), and they email you an **access key**.
2. Open `contact.html`, find `YOUR_ACCESS_KEY` and replace it with your key.

The key is designed to be public, so it is safe in a public GitHub repo. Messages go straight to your email; they are never stored in the repo or visible on the site.

## 2. Add your photos

Put `hero.jpg`, `why.jpg` and `about.jpg` in the `images/` folder. See `images/README.txt`.

## 3. Publish on GitHub Pages

1. Create a free account at github.com and click **New repository**. Name it e.g. `cheedhomecare`, set it to **Public**, and create it.
2. Click **uploading an existing file**, drag in **everything inside this folder** (not the folder itself), and click **Commit changes**.
3. Go to **Settings → Pages**. Under "Build and deployment", choose **Deploy from a branch**, branch **main**, folder **/ (root)**, and save.
4. In a minute your site is live at `https://YOUR-USERNAME.github.io/cheedhomecare/`.

## 4. Point cheedhomecare.com at it (Namecheap)

In Namecheap: **Domain List → Manage → Advanced DNS**.

1. Delete the old records pointing to Wix (A records for `@`, CNAME for `www`, any URL Redirect). **Leave MX/TXT email records alone.**
2. Add these:

| Type | Host | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | YOUR-USERNAME.github.io. |

3. Back in GitHub **Settings → Pages**, type `cheedhomecare.com` under **Custom domain** and save. After DNS updates (minutes to a few hours), tick **Enforce HTTPS**.

## Editing later

Text lives directly in the `.html` files, so you can edit it in GitHub's web editor (open the file, click the pencil icon, commit). Changes go live within a minute or two.

## Before going live

- **Testimonials** (home page): keep them only if they are real quotes from real clients who agreed to be named. Instructions for removing the section are in a comment in `index.html`.
- Check the Resources page links still work once in a while; government pages move.
