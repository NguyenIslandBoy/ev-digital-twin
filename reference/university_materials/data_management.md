# Data Management for Dissertation

A practical guide and reusable template for planning, collecting, storing, documenting, protecting, analysing, and sharing dissertation research data.

> **Purpose:** This file turns general Data Management Plan (DMP) guidance into a dissertation-focused workflow. It is suitable for undergraduate, MSc, MBA, and taught postgraduate dissertations.

---

## 1. What Is Research Data?

In a dissertation, **research data** means any material used as evidence to answer your research question, support your analysis, validate your findings, or allow another person to understand how your conclusions were produced.

Research data can include:

- Survey responses
- Interview recordings
- Interview transcripts
- Focus group notes
- Observation notes
- Experimental results
- Web-scraped datasets
- Public datasets
- Company documents
- Social media posts
- Images, videos, or audio files
- Code, scripts, notebooks, and models
- Cleaning logs and analysis outputs
- Consent forms and participant information sheets
- Data dictionaries and metadata files

A simple rule:

> If the material helps you produce, explain, validate, or reproduce your dissertation findings, treat it as research data.

---

## 2. Why Data Management Matters in a Dissertation

Data management is not just an administrative task. It protects the quality, credibility, and ethics of your dissertation.

A good data management plan helps you:

- Avoid losing files before submission
- Keep raw data, cleaned data, and analysis files separate
- Make your methodology easier to explain
- Improve the reliability of your findings
- Protect participant privacy
- Comply with university ethics requirements
- Prepare for viva, supervisor questions, or dissertation review
- Reuse your own data later for publication, portfolio projects, or further research

Poor data management can lead to:

- Missing or corrupted files
- Confusing file versions
- Inconsistent variable names
- Unclear data cleaning decisions
- Accidental disclosure of personal data
- Weak evidence for your findings
- Difficulty defending your methodology

---

## 3. Core Principle: Open as Possible, Closed as Necessary

Good dissertation research should be transparent where possible, but protected where necessary.

This means:

- Share methods, code, metadata, and non-sensitive outputs when appropriate.
- Restrict access to personal, confidential, commercially sensitive, or ethically restricted data.
- Explain clearly what can be shared, what cannot be shared, and why.

For example:

| Data Type | Can It Be Shared? | Typical Decision |
|---|---:|---|
| Anonymous survey results | Often yes | Share cleaned dataset if no risk of identification |
| Interview transcripts | Sometimes | Share only if consent allows and data are anonymised |
| Raw interview recordings | Usually no | Keep securely, delete after required retention period |
| Company internal files | Usually no | Store securely and describe only in aggregated form |
| Python/R analysis scripts | Usually yes | Share with dissertation appendix or repository |
| Data dictionary | Usually yes | Share to explain variables and coding |

---

## 4. Dissertation Data Lifecycle

Think of your data as moving through a lifecycle:

1. **Plan**  
   Decide what data you need, how you will collect it, where it will be stored, and what ethical issues exist.

2. **Create or Collect**  
   Gather data through surveys, interviews, scraping, experiments, public datasets, or document analysis.

3. **Process**  
   Clean, anonymise, validate, transform, transcribe, code, or merge data.

4. **Analyse**  
   Use statistical, qualitative, computational, or thematic methods to answer the research questions.

5. **Preserve**  
   Keep essential files safely until dissertation assessment is complete and for the required retention period.

6. **Share or Restrict**  
   Decide what can be shared, what must remain closed, and what should be deleted.

7. **Delete**  
   Delete personal or sensitive data when it is no longer needed or when ethics approval requires it.

---

## 5. Dissertation Data Management Plan: Main Sections

A strong DMP for a dissertation should answer six questions:

1. What data will be produced or reused?
2. How will the data be collected?
3. How will the data be documented and organised?
4. How will the data be stored and secured?
5. How will ethical, legal, and privacy issues be handled?
6. What will happen to the data after the dissertation is submitted?

The sections below provide a practical template.

---

# Part A — Data Description

## 6. What Data Will You Use?

Start by describing the data required for your dissertation.

### Questions to answer

- What data do you need to answer your research question?
- Will you collect new data, reuse existing data, or both?
- What format will the data be in?
- How much data do you expect?
- Will the data include personal, sensitive, or confidential information?
- Will the data include code, models, or software?

### Example: Quantitative Dissertation

> This dissertation will use survey data collected through an online questionnaire. The dataset will include demographic variables, Likert-scale responses, behavioural indicators, and open-text comments. The raw data will be exported as `.csv` from the survey platform. Cleaned data will be stored as `.csv` and analysis outputs will be generated using Python notebooks.

### Example: Qualitative Dissertation

> This dissertation will use semi-structured interview data from 8–12 participants. Data will include audio recordings, interview transcripts, field notes, and coding files. Recordings will be stored as `.mp3` or `.wav`; transcripts will be stored as `.docx` and `.pdf`; coding notes will be stored in spreadsheet or qualitative analysis software format.

### Example: Data Science Dissertation

> This dissertation will reuse publicly available datasets and collect additional web-based data using scraping scripts. Raw datasets will be stored separately from cleaned datasets. The project will also generate Python scripts, Jupyter notebooks, processed features, trained model outputs, evaluation metrics, visualisations, and documentation files.

---

# Part B — Data Collection

## 7. How Will Data Be Collected?

Your DMP should explain the data collection method clearly enough that another researcher could understand what you did.

### Include details about:

- Research design
- Data source
- Sampling strategy
- Participant group, if applicable
- Collection instruments
- Software or tools used
- Collection dates or expected timeline
- Conditions or context of data collection
- Permissions required
- Quality checks during collection

### Example: Survey Data

> Survey data will be collected using Microsoft Forms or Qualtrics. Participants will be recruited through university networks and social media. Before starting the survey, participants will read an information sheet and provide informed consent. The survey will remain open for two weeks. Responses will be exported as `.csv` files and stored in the secure dissertation folder.

### Example: Interview Data

> Interviews will be conducted online using Microsoft Teams or Zoom. With participant consent, interviews will be recorded and transcribed. Recordings will be used only for transcription and accuracy checking. Transcripts will be anonymised before analysis. A separate consent record will be stored securely and separately from the transcripts.

### Example: Public Dataset

> Public datasets will be downloaded from official repositories or reputable data providers. The original source, download date, licence, file format, and citation information will be recorded in a `data_sources.md` file. Raw downloaded data will not be edited directly.

---

## 8. Data Quality Control

Data quality is about making sure your data are accurate, consistent, complete, and suitable for analysis.

### Quantitative quality checks

- Check missing values
- Check duplicate rows
- Check impossible or invalid values
- Use consistent coding for categories
- Validate date, currency, and numerical formats
- Keep a cleaning log
- Save raw and cleaned data separately
- Use reproducible scripts where possible

### Qualitative quality checks

- Check transcripts against recordings
- Use consistent anonymisation rules
- Maintain a coding framework
- Keep memos explaining coding decisions
- Review a sample of coded data for consistency
- Document changes to interview guides or fieldwork procedures

### Data science quality checks

- Record data source and download date
- Check schema and data types
- Validate joins and merges
- Separate train, validation, and test data
- Avoid data leakage
- Track preprocessing steps
- Version analysis notebooks or scripts
- Save model evaluation outputs clearly

---

# Part C — Documentation and Organisation

## 9. What Documentation Should You Create?

Documentation makes your data understandable to your supervisor, marker, future self, or another researcher.

Create these files where relevant:

| File | Purpose |
|---|---|
| `README.md` | Explains the project folder and how files are organised |
| `data_sources.md` | Records where each dataset came from |
| `data_dictionary.csv` | Defines variables, values, units, and coding |
| `cleaning_log.md` | Explains how raw data became cleaned data |
| `analysis_log.md` | Records major analysis decisions |
| `consent_record.xlsx` | Tracks participant consent, stored separately and securely |
| `anonymisation_log.xlsx` | Tracks replacements of names or identifiers, stored securely |
| `codebook.md` | Explains qualitative themes or codes |
| `version_log.md` | Records important file versions |

---

## 10. File Naming Rules

Use file names that are short, meaningful, and consistent.

### Good file naming principles

- Use dates in `YYYY-MM-DD` format.
- Avoid spaces.
- Use hyphens or underscores.
- Include version numbers where useful.
- Do not use vague names such as `final_final_reallyfinal.docx`.
- Do not include participant names in file names.

### Good examples

```text
2026-05-20_survey_raw.csv
2026-05-21_survey_cleaned_v01.csv
2026-05-22_interview_P01_transcript_anonymised.docx
2026-05-23_model_evaluation_results.csv
2026-05-24_thematic_codebook_v02.md
```

### Bad examples

```text
data.csv
new data final.csv
John interview.docx
analysis final final updated.xlsx
```

---

## 11. Recommended Folder Structure

Use a clean folder structure from the beginning.

```text
dissertation_project/
│
├── 00_admin/
│   ├── ethics_approval/
│   ├── consent_forms/
│   └── supervisor_feedback/
│
├── 01_raw_data/
│   ├── surveys/
│   ├── interviews/
│   ├── public_datasets/
│   └── web_scraped_data/
│
├── 02_processed_data/
│   ├── cleaned/
│   ├── anonymised/
│   └── merged/
│
├── 03_documentation/
│   ├── README.md
│   ├── data_sources.md
│   ├── data_dictionary.csv
│   ├── cleaning_log.md
│   └── analysis_log.md
│
├── 04_analysis/
│   ├── notebooks/
│   ├── scripts/
│   ├── models/
│   └── outputs/
│
├── 05_results/
│   ├── tables/
│   ├── figures/
│   └── statistical_outputs/
│
├── 06_writeup/
│   ├── dissertation_draft.docx
│   ├── dissertation_final.pdf
│   └── appendix/
│
└── 07_archive/
    ├── submission_package/
    └── retained_data/
```

### Important rule

Keep these separate:

- Raw data
- Cleaned data
- Anonymised data
- Analysis files
- Consent records
- Final dissertation outputs

---

# Part D — Storage, Backup, and Security

## 12. Where Will Data Be Stored?

Choose secure storage depending on the sensitivity of the data.

### Suitable storage options

- University OneDrive
- University Teams site
- University research storage
- Encrypted external drive
- Secure institutional cloud storage
- Version-controlled repository for non-sensitive code

### Avoid

- Personal USB drives as the only copy
- Public GitHub repositories for sensitive data
- Emailing raw personal data to yourself
- Storing participant data on shared personal devices
- Saving confidential files in random download folders

---

## 13. Backup Strategy

Use the **3-2-1 backup rule** where possible:

- **3 copies** of important files
- **2 different storage locations**
- **1 copy separate from your main working device**

### Minimum dissertation backup plan

| File Type | Main Copy | Backup Copy | Frequency |
|---|---|---|---|
| Raw data | University cloud storage | Encrypted local backup | After every collection session |
| Cleaned data | Project folder | University cloud backup | After every major cleaning step |
| Analysis scripts | Git/private repository | Local project folder | After every major change |
| Dissertation draft | University cloud storage | Local backup | Daily during writing |
| Consent forms | Secure restricted folder | Encrypted backup if allowed | After collection |

---

## 14. Access Control

Only people who need access should have access.

For most dissertations:

- The student should access the full working dataset.
- The supervisor may access anonymised or necessary files.
- Participants should not access other participants' data.
- Raw identifiable data should not be shared casually.
- Any transcription service must be approved and confidentiality-compliant.
- Sensitive files should be password-protected or encrypted.

---

# Part E — Ethics, Privacy, and Legal Compliance

## 15. Personal and Sensitive Data

Personal data means information that can identify a person directly or indirectly.

### Direct identifiers

- Name
- Email address
- Student number
- Phone number
- Address
- Face image
- Voice recording
- Signature

### Indirect identifiers

- Job title
- Workplace
- Age
- Nationality
- Location
- Rare demographic combination
- Highly specific personal story

Sensitive data may include information about health, ethnicity, politics, religion, sexuality, criminal records, biometrics, or other protected characteristics.

For dissertation work, avoid collecting sensitive data unless it is necessary, justified, and approved by ethics review.

---

## 16. Consent and Participant Information

For research involving people, your DMP should match your ethics application.

Participants should understand:

- What data you will collect
- Why you are collecting it
- How it will be used
- Whether participation is voluntary
- Whether they can withdraw
- How long data will be retained
- Who can access the data
- Whether data will be anonymised
- Whether data may be quoted in the dissertation
- Whether data will be archived or shared

### Practical consent checklist

- [ ] Participant information sheet prepared
- [ ] Consent form prepared
- [ ] Consent collected before data collection
- [ ] Consent records stored separately from research data
- [ ] Withdrawal process explained
- [ ] Quotation permission clarified
- [ ] Audio/video recording permission clarified
- [ ] Data sharing or archiving permission clarified

---

## 17. Anonymisation

Anonymisation reduces the risk of identifying participants.

### Common anonymisation actions

- Replace names with participant IDs, e.g. `P01`, `P02`
- Remove email addresses and phone numbers
- Generalise locations, e.g. “a city in Northern England”
- Generalise job titles where needed
- Remove or paraphrase highly identifiable stories
- Aggregate demographic categories
- Store the participant key separately and securely

### Example

Original:

> “My name is Linh Nguyen, and I work as the only Vietnamese marketing intern at Company X in Newcastle.”

Anonymised:

> “Participant P03 described working as an international marketing intern at a UK-based company.”

---

## 18. Confidential or Third-Party Data

Some dissertations use company, platform, or third-party data. This can create restrictions.

Before using third-party data, check:

- Do you have permission to use it?
- Is the data public or private?
- Does the platform allow scraping or reuse?
- Are there copyright restrictions?
- Are there terms of service restrictions?
- Can the data be quoted in the dissertation?
- Can it be shared in an appendix?
- Does it include personal information?

When in doubt, describe data in aggregated form rather than exposing raw records.

---

# Part F — Analysis and Reproducibility

## 19. Managing Analysis Files

Your analysis should be traceable from raw data to findings.

### Good practice

- Never edit raw data directly.
- Use scripts for cleaning where possible.
- Save cleaned data as a new file.
- Keep a log of manual edits.
- Record analysis decisions.
- Save figures and tables with clear names.
- Store code and outputs in organised folders.
- Use version numbers for major changes.

### Example analysis workflow

```text
raw_survey.csv
    ↓
cleaning_script.ipynb
    ↓
survey_cleaned_v01.csv
    ↓
analysis_script.ipynb
    ↓
regression_results.csv
    ↓
figure_01_customer_intention.png
    ↓
dissertation_results_chapter.docx
```

---

## 20. Version Control

Use simple version control even if you do not use Git.

### Simple versioning

```text
survey_cleaned_v01.csv
survey_cleaned_v02.csv
survey_cleaned_v03.csv
```

### Better versioning for code

Use Git for:

- Python scripts
- R scripts
- SQL files
- Jupyter notebooks
- Markdown documentation
- Non-sensitive project notes

Do **not** upload sensitive data to public repositories.

---

# Part G — Preservation, Sharing, and Deletion

## 21. What Happens After Submission?

Before submitting your dissertation, decide what to keep, share, restrict, or delete.

### Keep

- Final dissertation
- Final anonymised dataset, if appropriate
- Data dictionary
- Cleaning log
- Analysis scripts
- Final figures and tables
- Ethics approval documents
- Consent records for the required retention period

### Share, if appropriate

- Anonymised data
- Code
- Data dictionary
- README file
- Non-sensitive appendices
- Survey instrument
- Interview guide

### Restrict

- Raw identifiable data
- Consent forms
- Participant contact details
- Confidential company data
- Commercially sensitive information
- Raw audio/video recordings

### Delete

- Personal data no longer needed
- Temporary files
- Duplicate working files
- Unnecessary recordings after transcription and checking, if ethics approval requires deletion

---

## 22. Choosing a Repository

If your university or supervisor expects data sharing, consider:

- University repository
- Open Science Framework
- Zenodo
- Figshare
- UK Data Service
- Discipline-specific repositories
- GitHub or GitLab for code only, where appropriate

Do not upload sensitive or confidential data unless it has been properly anonymised and sharing is ethically approved.

---

# Part H — Roles, Responsibilities, and Timeline

## 23. Who Is Responsible?

For a dissertation, the responsibility is usually simple but should still be stated.

| Responsibility | Person |
|---|---|
| Data collection | Student researcher |
| Secure storage | Student researcher |
| Ethics compliance | Student researcher, with supervisor guidance |
| Data cleaning | Student researcher |
| Data documentation | Student researcher |
| Data analysis | Student researcher |
| Data backup | Student researcher |
| Data sharing decision | Student researcher and supervisor |
| Data deletion | Student researcher |

---

## 24. Suggested Timeline

| Stage | Data Management Task |
|---|---|
| Before ethics application | Draft DMP, identify data types, prepare consent materials |
| Before collection | Set up folders, naming rules, storage, backup plan |
| During collection | Store data securely, record consent, maintain collection log |
| During cleaning | Preserve raw data, create cleaned copies, update cleaning log |
| During analysis | Save scripts, outputs, figures, and analysis decisions |
| Before submission | Check anonymisation, prepare appendix files, finalise documentation |
| After submission | Archive essential files, delete unnecessary personal data |

---

# Part I — Ready-to-Use Dissertation DMP Template

Copy and complete the template below.

---

## Dissertation Data Management Plan Template

### 1. Project Information

**Dissertation title:**  
`[Insert title]`

**Student researcher:**  
`[Insert name]`

**Programme:**  
`[Insert programme]`

**Supervisor:**  
`[Insert supervisor name]`

**Research question:**  
`[Insert research question]`

---

### 2. Data Description

This dissertation will use the following data:

| Data | Source | Format | Estimated Size | Sensitive? |
|---|---|---|---:|---|
| `[e.g. Survey responses]` | `[e.g. Qualtrics]` | `.csv` | `[e.g. 200 responses]` | `[Yes/No]` |
| `[e.g. Interview transcripts]` | `[e.g. Participants]` | `.docx/.pdf` | `[e.g. 10 interviews]` | `[Yes/No]` |
| `[e.g. Analysis code]` | `[e.g. Student-created]` | `.ipynb/.py` | `[e.g. 10 files]` | `No` |

---

### 3. Data Collection Method

Data will be collected by:

`[Explain how you will collect or obtain the data. Include tools, participants, sources, dates, and permissions.]`

Quality will be controlled by:

`[Explain validation, checking, transcription review, coding consistency, or data cleaning procedures.]`

---

### 4. Documentation and Organisation

The project will use the following documentation:

- `README.md` to explain the folder structure
- `data_sources.md` to record dataset sources
- `data_dictionary.csv` to define variables
- `cleaning_log.md` to document cleaning decisions
- `analysis_log.md` to record analysis decisions

Files will be named using:

```text
YYYY-MM-DD_description_version.format
```

Example:

```text
2026-06-01_survey_cleaned_v01.csv
```

---

### 5. Storage and Backup

Data will be stored in:

`[Insert storage location, e.g. university OneDrive, encrypted drive, research storage.]`

Backup plan:

`[Explain how often data will be backed up and where backup copies will be kept.]`

Access will be limited to:

`[Explain who can access raw, cleaned, anonymised, and final data.]`

---

### 6. Ethics, Privacy, and Legal Compliance

This project involves:

- [ ] No personal data
- [ ] Personal data
- [ ] Sensitive personal data
- [ ] Confidential company data
- [ ] Third-party data
- [ ] Public data only

Ethical safeguards:

`[Explain consent, anonymisation, participant information, withdrawal, confidentiality, and data protection steps.]`

Anonymisation plan:

`[Explain how names, identifiers, locations, organisations, or personal details will be removed or generalised.]`

---

### 7. Analysis and Reproducibility

Analysis will be conducted using:

`[Insert software, e.g. Excel, SPSS, NVivo, Python, R, SQL, Power BI.]`

To support reproducibility:

`[Explain how scripts, notebooks, data dictionaries, logs, and outputs will be saved.]`

---

### 8. Preservation, Sharing, and Deletion

After submission:

| Data Type | Action |
|---|---|
| Raw identifiable data | `[Keep securely / delete / restrict]` |
| Consent forms | `[Keep securely for required period]` |
| Anonymised dataset | `[Archive / share / restrict]` |
| Analysis code | `[Keep / share]` |
| Final figures and tables | `[Keep / include in appendix]` |
| Temporary files | `[Delete]` |

Data will be retained for:

`[Insert required period based on university policy or ethics approval.]`

Data will be shared only if:

`[Explain conditions for sharing, e.g. anonymised, consented, non-confidential, supervisor-approved.]`

---

# Part J — Final Checklist Before Submission

Use this checklist before submitting your dissertation.

## Data and Files

- [ ] Raw data is saved and unchanged
- [ ] Cleaned data is saved separately
- [ ] Anonymised data is saved separately
- [ ] Analysis files are clearly named
- [ ] Figures and tables are saved in final format
- [ ] Dissertation appendix files are complete

## Documentation

- [ ] README file completed
- [ ] Data dictionary completed
- [ ] Data sources recorded
- [ ] Cleaning log completed
- [ ] Analysis decisions recorded
- [ ] Codebook completed, if qualitative research is used

## Ethics and Security

- [ ] Consent forms stored separately
- [ ] Identifiable data protected
- [ ] Data anonymised where required
- [ ] Sensitive data not uploaded publicly
- [ ] Confidential company data restricted
- [ ] Data retention and deletion plan confirmed

## Reproducibility

- [ ] Analysis can be traced from raw data to final results
- [ ] Code or manual analysis steps are documented
- [ ] Final tables and charts match the dissertation text
- [ ] Any excluded data are explained
- [ ] Any transformations are documented

## Archiving

- [ ] Final dissertation saved as PDF
- [ ] Final dataset archived or restricted
- [ ] Scripts/notebooks archived
- [ ] Unnecessary temporary files deleted
- [ ] Personal data deletion date recorded, if applicable

---

# Part K — Example Short DMP Statement for a Dissertation

You can adapt the following paragraph for a methodology chapter or ethics form.

> This dissertation will follow a structured data management plan covering data collection, storage, documentation, security, analysis, and retention. Raw data will be stored separately from cleaned and anonymised datasets. All files will follow a consistent naming convention and will be organised in a secure project folder. Personal or identifiable information will be minimised, stored separately from research data, and anonymised before analysis where appropriate. Data quality will be maintained through validation checks, cleaning logs, and documented analysis procedures. Access to sensitive data will be restricted to the student researcher and, where necessary, the supervisor. After submission, essential anonymised research materials and analysis documentation will be retained according to university requirements, while unnecessary personal or temporary files will be securely deleted.

---

# Part L — Stronger Example for Data Science Dissertation

> This dissertation will use publicly available datasets and student-generated analysis scripts. Original datasets will be stored unchanged in a raw data folder, while cleaned and transformed datasets will be stored separately. Data sources, licences, download dates, and preprocessing steps will be documented in a data sources file and cleaning log. Analysis will be conducted using Python, with notebooks and scripts saved in a version-controlled private repository. Model training, evaluation metrics, and visualisation outputs will be stored in clearly labelled folders. Since the project does not involve human participants, no consent forms are required; however, all third-party dataset licences and usage restrictions will be respected. After submission, code, documentation, and non-sensitive processed data may be shared in a public repository if permitted by the original data licences.

---

# Part M — Stronger Example for Interview-Based Dissertation

> This dissertation will collect semi-structured interview data from adult participants. Interviews will be recorded only with explicit consent and transcribed for analysis. Audio files will be stored securely and used only for transcription and accuracy checking. Transcripts will be anonymised by replacing names and identifiable details with participant codes. Consent forms and participant contact details will be stored separately from interview data. Only anonymised transcripts will be used for thematic analysis and dissertation writing. Direct quotations will be included only where they do not reveal participant identity. Raw recordings and identifiable materials will not be shared publicly and will be deleted or retained according to the approved ethics protocol.

---

## Final Advice

A dissertation DMP does not need to be long, but it must be specific. The strongest plans clearly explain:

1. What data you will use
2. How you will collect or obtain it
3. How you will keep it organised
4. How you will protect it
5. How you will document your decisions
6. What will happen to the data after submission

The goal is simple: your data should be safe, understandable, ethically managed, and strong enough to support your dissertation findings.
