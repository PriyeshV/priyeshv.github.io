# Priyesh Vijayan — research website

A responsive, multi-page academic website for GitHub Pages. The recommended architecture is **Jekyll with a shared layout and structured publication data**, rather than a single growing `index.md`. There is no JavaScript framework, analytics, external font dependency, or backend. JavaScript only enables publication filtering and the active navigation marker; every publication remains readable without it.

## Why Jekyll

This is a content-led academic site. GitHub Pages builds Jekyll directly, so maintaining it does not require an npm toolchain or a custom deployment workflow. Astro would be a good option if the site later gains substantial interactive demos or a larger component system; it adds a build step that is unnecessary here. A single Markdown file remains suitable for a short biography, but becomes cumbersome for this publication archive and the research narratives.

## Contents

- `index.html`: introduction, selected publications, updates, contact.
- `research.html`: research overview and emerging LLM interests.
- `projects/`: four detailed research/project pages.
- `publications.html`: searchable archive of 19 records, including historical workshop and preprint versions. This is not a count of 19 distinct peer-reviewed papers.
- `teaching.html`: two-column teaching list, service, reviewer recognition.
- `background.html`: education, experience, earlier projects, talks, patent, coursework.
- `_data/publications.json`: the single publication source, loaded automatically by Jekyll.
- `_data/project-*.json`: publication IDs associated with each project.
- `_layouts/default.html`: shared metadata, navigation, and footer.
- `_includes/`: publication rendering templates.
- `assets/`: responsive CSS, small JavaScript enhancement, favicon. The research illustration is inline SVG.
- `reference/`: original supplied Markdown and both LaTeX CV versions, excluded from the deployed site. The original contact details remain in these reference files; do not upload the reference folder to a public repository unless you intend those files to be public.
- `CONTENT-NOTES.md`: citation corrections, source decisions, and details to confirm.
- `preview/`: pre-rendered static copy for immediate inspection. It is excluded from Jekyll builds.

## Deploy to your existing GitHub Pages site

1. Back up the current `priyeshv.github.io` repository, including its PDFs and any `CNAME` file.
2. Copy the contents of this directory into the repository root. Preserve existing PDFs and research assets. Remove the old root `index.md` (or other conflicting home page) from that repository after backing it up: this package supplies `index.html`.
3. The included `_config.yml` already sets `url: https://priyeshv.github.io` and `baseurl: ""`. Preserve or add any existing custom-domain settings you use.
4. In GitHub, open **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, then select your main branch and **/(root)**.
5. Commit and push. GitHub's Pages build processes the Liquid templates and publishes the site. Check the build result under **Actions**, then open the URL shown in Pages settings.
6. Verify the navigation, publication filters, CV link, and thesis link on the deployed site. The CV remains linked to `https://priyeshv.github.io/CV.pdf`; this package does not compile or replace that PDF.

Do not add `.nojekyll` when deploying the Jekyll source. No Site hosting account or third-party deployment service is required.

### Deploy as a project repository instead

For a repository named `research-site`, keep `url: https://priyeshv.github.io` and change `baseurl: /research-site`. The shared templates use Jekyll's `relative_url` filter so navigation and assets work under that prefix. For another account, change `url` accordingly. Before deleting the old personal site, replace the externally hosted CV/thesis URLs with local assets or a stable new URL.

## Preview locally with Jekyll

Install a supported Ruby and Bundler, then from this folder run:

```sh
bundle install
bundle exec jekyll serve
```

Open the local address printed by Jekyll (normally `http://127.0.0.1:4000`). GitHub Pages chooses its supported Jekyll versions through the `github-pages` gem.

### Preview without Ruby

Python 3 is sufficient for an immediate static preview:

```sh
python3 scripts/preview.py
python3 -m http.server 8000 --directory preview
```

Open `http://localhost:8000`. The helper mirrors the limited templates used by this site; it is not a general-purpose Jekyll/Liquid interpreter. Use a real Jekyll build to validate any future template changes. To inspect project-repository URLs, run `python3 scripts/preview.py --baseurl /research-site` and open `http://localhost:8000/research-site/`.

The generated `preview/` can also be served by any static host. If publishing those generated files directly on GitHub Pages, upload the contents of `preview/` as the publishing root and add `.nojekyll` there. The recommended ongoing workflow is the Jekyll source instead.

## Maintain the content

### Add a publication

Add an object to `_data/publications.json` in the desired display order. Use a unique stable `id`, exact title, ordered author string, integer year, venue, topic, links, and optional note. An example:

```json
{
  "id": "p20",
  "title": "Exact published title",
  "authors": "Authors in publication order",
  "year": 2027,
  "venue": "Exact venue and publication status",
  "topic": "Graph learning",
  "links": {"Paper": "https://example.org/paper"},
  "note": ""
}
```

Do not add unavailable links as empty strings. Add the new year and any new topic to the filter options in `publications.html`; change its fallback record count. Update `_includes/selected-publications.html` to change featured IDs. Add an ID to the appropriate `_data/project-*.json` to show it on a project page. All appearances share the same record. Re-run the Python helper only when you want to refresh the standalone preview; Jekyll consumes the data directly.

### Other edits

Edit the relevant page's body text while retaining its front matter (`---` block). Change common navigation and contact links in `_layouts/default.html`. Change colors, typography, and spacing in `assets/style.css`. Keep LLM research as an emerging direction until there is concrete work to describe. The current copy does not invent LLM publications, employment, research metrics, or performance improvements.

## Validation and limitations

The delivery includes a checked static rendering of nine pages, internal-link/anchor and asset checks at both root and project-repository paths, JavaScript syntax validation, and browser inspection of desktop/mobile layout and publication filters. Search returned the single Laplacian record; combined filters displayed the empty state; the Evaluation filter returned three records. The local machine did not have Jekyll installed, so an actual Jekyll build was not run; the GitHub Pages build remains the final deployment check. Some external publishers require browser verification, and historical links have not all been independently validated. See `CONTENT-NOTES.md` for source-specific decisions. No public deployment has been performed.
