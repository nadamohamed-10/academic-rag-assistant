# Phase 1 — Verification Report
## Academic Research RAG Corpus: AI/ML in Healthcare

## Dataset Summary

- **Number of papers:** 24
- **Year range:** 2017–2025 (one foundational paper from 2017; bulk from 2020–2025)
- **Main categories:**
  - Medical imaging + AI (4 papers)
  - ML/DL for diagnosis & prediction (5 papers)
  - Deep learning in healthcare / EHR (4 papers)
  - Bioinformatics / multi-omics (4 papers)
  - Explainable AI (XAI) in healthcare (3 papers)
  - Clinical decision support (2 papers)
  - Medical image segmentation / detection (2 papers)
- **Main AI/ML methods represented:** CNNs, self-supervised learning, ensemble methods (bagging/boosting/stacking/voting), classical ML (RF, LR, SVM, KNN, XGBoost), RNNs (LSTM/GRU) for EHR sequences, autoencoders and variational autoencoders, graph neural networks, Segment Anything Model (SAM)-based foundation models, SHAP/LIME/Grad-CAM explainability methods, multi-task Cox survival models.
- **Main healthcare applications:** medical image classification/segmentation (radiology, dermatology, gastrointestinal, brain tumor), cardiovascular/heart disease, Parkinson's disease, chronic disease risk prediction (UK Biobank), EHR-based disease onset and readmission prediction, cancer genomics/multi-omics, ICU mortality prediction, clinical decision support system usability and trust.

## Quality Checks

- **Number with verified full text (open-access, PDF confirmed accessible):** 24 / 24. All papers were located on PubMed Central (PMC), arXiv, or journals indexed in DOAJ (PLOS, Frontiers, MDPI journals, npj Digital Medicine, BMC), all of which provide free full-text PDFs.
- **Number with selectable/extractable text ("Yes"):** 22 / 24
- **Number marked "Probably" (uncertain extraction quality):** 1 / 24 (paper_002 — some reference tables may need care)
- **Number with uncertain/unverified DOI:** 4 / 24 (paper_002, paper_018, paper_020, paper_023, paper_024 are arXiv preprints without a confirmed peer-reviewed DOI at time of collection — noted as "Not verified" rather than guessed)
- **Number of duplicates removed:** Several near-duplicate "deep learning + medical imaging" survey candidates were considered and excluded in favor of more distinct entries to preserve topical diversity (e.g., multiple generic "review of DL in medical imaging" papers were narrowed down to the two most-cited/complementary ones — Litjens et al. 2017 and Imran Ul Haq 2022 — rather than including 4–5 overlapping surveys).
- **Verification method:** Each paper's title, author list, publication year, journal, and DOI were cross-checked against at least one authoritative source (PMC metadata page, arXiv abstract page, or publisher/DOI resolver page) via live web search and, for several papers, direct page fetches. No titles, authors, or DOIs were fabricated; fields that could not be confirmed are explicitly marked "Not verified" in the metadata rather than filled in with a guess.

## Common PDF Issues Likely to Appear in This Corpus

- **Two-column layout:** Common in arXiv preprints and IEEE/ACM-style papers (e.g., paper_001, paper_002, paper_023, paper_024) — can interleave text between columns if extracted naively; column-aware extraction is recommended.
- **Large tables:** Several papers (paper_005, paper_006, paper_009) contain wide, multi-row comparison tables (ensemble method performance breakdowns, algorithm catalogues) that may not extract cleanly into linear text and could benefit from separate table-parsing.
- **Figures and figure captions:** All papers contain diagrams (architecture diagrams, PRISMA flow diagrams, taxonomy figures); captions are usually extractable but images themselves are not text.
- **Equations:** Minimal in the review/survey papers selected; more likely in paper_016 (VAE loss functions) and paper_012/paper_017 (autoencoder formulations).
- **References/bibliographies:** All papers have long reference lists (30–300+ entries for the survey papers) which will be extracted as trailing text and should be filtered out or chunked separately during the cleaning stage.
- **Headers/footers:** PMC and arXiv PDFs typically include running headers (journal name, page numbers, PMCID) that should be stripped during cleaning.
- **Supplementary material:** A few papers (e.g., paper_005, paper_017) reference supplementary tables/figures hosted separately — these are not included in the collected PDFs.

## Data Collection Notes / Limitations

- **Search method:** Papers were identified via targeted web searches against PubMed Central, arXiv, and journal publisher pages (Frontiers, MDPI, PLOS, Nature/npj, BMC, Elsevier-hosted-but-OA), followed by direct verification fetches for bibliographic details.
- **Category balance:** Segmentation/detection and clinical-decision-support categories have 2 papers each rather than the requested 2–3, since maintaining strict verification standards (declining to include papers whose authors/DOIs could not be confirmed) took priority over hitting exact category counts. Coverage is otherwise close to the requested distribution.
- **arXiv preprints without confirmed DOI:** Five papers (paper_002, paper_018, paper_020, paper_023, paper_024) are arXiv preprints. Where a peer-reviewed version likely exists (e.g., paper_018 appears headed to ACM Computing Surveys, paper_020 to an AMIA proceedings), no DOI could be confirmed with certainty, so these are marked "Not verified" rather than guessed. The arXiv PDF links themselves are confirmed live and open-access.
- **PDF text-extractability:** Assessed by source type and known formatting (PMC/arXiv HTML+PDF pipelines reliably produce selectable text) rather than by downloading and OCR-testing every file, per the "no OCR" instruction. Actual extraction behavior should still be spot-checked during Phase 2 ingestion.
- **Recency:** Several papers are from 2025 (paper_009, paper_014, paper_016, paper_019, paper_020), reflecting deliberate inclusion of very current work; one foundational 2017 paper (paper_001) was retained per the "small number of older foundational papers" guidance.

## Recommendation

This 24-paper corpus is reasonably diverse across the seven target sub-domains (imaging, diagnosis/prediction, general healthcare DL/EHR, multi-omics/bioinformatics, XAI, clinical decision support, and segmentation/detection), draws from a healthy mix of repository types (PMC journal articles and arXiv preprints), and spans foundational (2017) through very recent (2025) work. All entries were positively verified to exist with correct core bibliographic metadata and a working open-access full-text link; nothing was invented. The main gaps are: (1) a modest shortfall in the segmentation/detection and clinical-decision-support categories (2 papers each instead of 2–3), and (2) five arXiv preprints lacking a confirmed peer-reviewed DOI. Neither gap should block proceeding to Phase 2 (PDF ingestion → text extraction → cleaning → chunking → embeddings → retrieval), but the team may want to run one additional targeted search pass specifically for segmentation and CDS papers with confirmed peer-reviewed DOIs before finalizing the corpus, and should apply column-aware PDF parsing given how many entries use two-column layouts.
