# TrustFlow Document Agent Implementation Plan (DOCUMENT\_AGENT\_PLAN.md)

## 1. Executive Summary & Goals

This plan outlines the architecture, required tools, and phased roadmap for integrating comprehensive support for remote (Google Workspace) and local (Word, Excel, PDF) documents into the TrustFlow system. The primary goal is to enable the AI agent to:

1.  **Read/Extract**: Programmatically access the structure (headings, tables, text blocks, cells) and content of all supported document types.
2.  **Edit/Manipulate**: Perform surgical or generative edits, such as replacing text, inserting new paragraphs, modifying spreadsheet cells, or updating slides.
3.  **Create/Write**: Generate new documents or save modified documents back to their source (Google Drive or local file system).

## 2. Architectural Overview: The Document Agent Module

We will introduce a new, isolated service layer called the **"Document Agent Module" (DAM)**. This module will standardize interactions, insulating the core TrustFlow agent logic from the complexities and unique APIs of each document type.

### Recommended Structure

```
TrustFlow Core
  |
  +-- Document Agent Module (DAM) [Python Service/Microservice]
      |
      +-- 1. API/Interface Layer (Standardized CRUD for Documents)
      |
      +-- 2. Adapter Layer (Handles API calls to specific services/libraries)
      |     |
      |     +-- Google Workspace Adapter (API calls, OAuth handling)
      |     |
      |     +-- Local DOCX Adapter (python-docx)
      |     |
      |     +-- Local XLSX Adapter (openpyxl/pandas)
      |     |
      |     +-- Local PDF Adapter (PyMuPDF)
      |
      +-- 3. Canonical Data Model (CDM) [JSON/Markdown]
```

## 3. Data Serialization and Interchange: Canonical Data Model (CDM)

To allow the AI agent to interact with different document types uniformly, all documents must be converted to a single **Canonical Data Model (CDM)** for reading, and the agent's edits must be expressed in a standardized format for writing.

### A. Document (Docs/Word/PDF) CDM

We recommend a structured **Markdown** format with embedded metadata (JSON) for maximum agent readability and preservation of structural elements (headings, lists, tables).

| Element | Read/Write Strategy |
| :--- | :--- |
| **Headings** | Extracted as Markdown headers (`#`, `##`) |
| **Paragraphs** | Extracted as plain text blocks. |
| **Tables** | Extracted as Markdown tables, preserving headers. |
| **Edits** | Represented as "JSON Patch" or "Intent-based" objects. E.g., `{"action": "replace", "target_id": "p3_uuid", "new_content": "..."}`. |

### B. Spreadsheet (Sheets/Excel) CDM

Spreadsheets are inherently structured. The CDM should be a **DataFrame-like JSON structure** to represent sheets, rows, columns, and cell values.

```json
{
  "spreadsheet_id": "...",
  "sheets": [
    {
      "sheet_name": "Sheet1",
      "data": [ ["Header1", "Header2"], [1, 2], [3, 4] ]
    }
  ]
}
```

## 4. Required Tools and Libraries

| Target System | Document Type | Functionality | Recommended Python Library | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Google Workspace** | Docs, Sheets, Slides | Read, Edit, Write | `google-api-python-client` | Requires OAuth 2.0 implementation. Utilize the specific Docs, Sheets, and Slides APIs. |
| **Local Files** | Word (.docx) | Read, Edit, Write | `python-docx` | Excellent for structural editing and content manipulation. |
| **Local Files** | Excel (.xlsx, .xlsm) | Read, Edit, Write, Data Manipulation | `openpyxl`, `pandas` | `openpyxl` for direct cell manipulation. `pandas` for bulk data operations (reading entire sheet into a DataFrame). |
| **Local Files** | PDF (.pdf) | Structured Read (Extraction), Manipulation | `PyMuPDF` (or `fitz`), `pypdf` | **Extraction:** `PyMuPDF` provides structured text and layout awareness. **Editing:** Direct text editing is complex; for major changes, extract, edit in CDM, then regenerate (or export as DOCX/TXT). `pypdf` for simple tasks (merge, split). |

## 5. Component Deep Dive

### 5.1. Google Workspace Integration

This is the most critical component due to authentication requirements and API complexity.

#### Authentication Strategy

1.  **Protocol**: Implement **OAuth 2.0** with Service Account or a standard web application flow (recommended for end-user interaction).
2.  **Scopes**: Access should be scoped strictly to the documents required (e.g., `https://www.googleapis.com/auth/documents`, `https://www.googleapis.com/auth/spreadsheets`).
3.  **Token Management**: Securely store and refresh access tokens using the TrustFlow credential management system.

#### Document API Strategy

| Document Type | Key API Method | Strategy |
| :--- | :--- | :--- |
| **Docs** | `documents.get`, `documents.batchUpdate` | Read the document content and structure, convert to CDM (Markdown). Use `batchUpdate` for generative edits, which allows for precise control over insertions and replacements. |
| **Sheets** | `spreadsheets.values.get`, `spreadsheets.values.batchUpdate` | Read specific ranges or entire sheets. Convert to DataFrame-like CDM. Use `batchUpdate` for efficient cell writing. |
| **Slides** | `presentations.get`, `presentations.batchUpdate` | Extract slide structure (text, titles, images). Editing involves complex positioning and element manipulation via `batchUpdate` requests. |

### 5.2. Local Document Integration

The strategy here is to download the local file (from the user's workspace or a local path) and process it using the dedicated open-source libraries.

| File Type | Read/Extraction Process | Write/Edit Process |
| :--- | :--- | :--- |
| **DOCX** | Use `python-docx` to iterate through paragraphs, runs, and tables. Extract style information (e.g., "Heading 1") and map to CDM (Markdown). | The agent generates a set of change objects against the CDM. The DOCX adapter applies these changes using `python-docx` methods (e.g., `paragraph.clear(); paragraph.add_run(...)`). |
| **XLSX** | Use `pandas.read_excel` for high-performance extraction of sheet data into DataFrames, which are then converted to the CDM JSON structure. | Convert the agent's CDM changes back into a DataFrame or direct cell writes, then use `openpyxl` to write back to the XLSX file. |
| **PDF** | Use `PyMuPDF`'s layout-aware extraction functions (`to_markdown` or block-based text fetching) to create a structured CDM. | **Limited Editing:** PDF is an endpoint format. TrustFlow should focus on *generation* (e.g., using ReportLab or FPDF to create a new PDF from edited content) or *annotation* rather than true text-reflow editing. |

## 6. Implementation Roadmap

The implementation should be phased to manage complexity and provide incremental value.

### Phase 1: Read-Only Integration

| Step | Description | Deliverable |
| :--- | :--- | :--- |
| **1.1 Core Setup** | Create the Document Agent Module (DAM) service shell and define the Canonical Data Model (CDM) schemas. | DAM Service Skeleton, CDM Schemas (JSON/TS) |
| **1.2 Google Read** | Implement OAuth and read-only adapters for Docs, Sheets, and Slides. Focus on extracting text and tabular data into the CDM. | TrustFlow can read and summarize Google Workspace documents. |
| **1.3 Local Read** | Implement read-only adapters for DOCX, XLSX (using pandas/openpyxl), and structured PDF extraction (using PyMuPDF). | TrustFlow can read and summarize local documents. |
| **1.4 Testing** | Develop unit and integration tests for all read operations and CDM fidelity. | Baseline Document Reading Capability. |

### Phase 2: Edit and Write (Core Functionality)

| Step | Description | Deliverable |
| :--- | :--- | :--- |
| **2.1 Edit Protocol** | Define the standardized "Edit Intent" object format for the agent to express changes (e.g., insert, replace, delete). | Document Edit Protocol (JSON Schema). |
| **2.2 Google Write** | Implement `batchUpdate` logic for Docs (text edits) and Sheets (cell updates). | TrustFlow can edit Google Docs and Sheets. |
| **2.3 Local Write** | Implement editing and saving logic for DOCX (`python-docx`) and XLSX (`openpyxl`). | TrustFlow can edit local Word and Excel files. |

### Phase 3: Advanced Features and PDF Editing/Generation

| Step | Description | Deliverable |
| :--- | :--- | :--- |
| **3.1 Slides/Presentation** | Implement reading and editing logic for Slides (structure, titles, text boxes). | TrustFlow can modify presentations. |
| **3.2 PDF Generation** | Integrate a PDF generation library (e.g., ReportLab) to enable "Save as PDF" functionality from any CDM. | TrustFlow can create new PDF reports. |
| **3.3 Media Handling** | Add support for extracting image URLs (Google) or embedded images (DOCX) and inserting new media. | Full document fidelity, including images. |
| **3.4 Performance** | Optimize for large files and parallel processing where possible. | Production-ready DAM. |

## 7. Security and Compliance

### Google Workspace (OAuth)
*   **Principle of Least Privilege**: Request the narrowest OAuth scopes necessary (e.g., avoid `.../auth/drive` if only content is needed).
*   **Credential Storage**: OAuth tokens must be encrypted at rest and handled securely, ideally via a dedicated secrets manager in the TrustFlow architecture.

### Local Documents
*   **File Isolation**: Local file processing must occur within a sandboxed environment to prevent file system traversal or compromise from malformed documents.
*   **Data Masking**: Implement logging rules to prevent sensitive document content from being logged during processing, especially in the raw CDM or error logs.
