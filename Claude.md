QR Attendance System - Project Context
Project Overview

Name: QR Attendance System
Description: Digital attendance ecosystem for universities with QR-based check-in system
Tech Stack:

Frontend: React (Web Panel for Professors/Admin)
Mobile: Flutter (Student App)
Backend: Django REST Framework
Database: MySQL
Auth: JWT
Security: HMAC-signed QR codes



Architecture Overview
System Components

Flutter Mobile App (Students)

Authorization
QR Scanner
Attendance recording
Attendance history
Profile management


React Web Panel (Professors & Admin)

Professor: Today's lectures → Start Session → Generate QR
Professor: Live attendance monitoring
Admin: Users, Courses, Schedule, Enrollment management
Admin: System statistics and export


Django REST Backend API

CRUD operations for all models
HMAC QR code generation
Session logic (Start Session only - no manual stop)
Attendance scan validation
Export endpoints


MySQL Database

Users, Courses, Enrollment
Timetable, Sessions, Attendance



Code Conventions
Naming

Files: [e.g., kebab-case, PascalCase]
Variables: [e.g., camelCase]
Constants: [e.g., UPPER_SNAKE_CASE]
Components: [e.g., PascalCase]

Style Guidelines

[Indentation: spaces/tabs, size]
[Quotes: single/double]
[Semicolons: yes/no]
[Line length limit]

Patterns to Follow

[State management approach]
[Error handling patterns]
[API call patterns]
[Testing conventions]

Dependencies & Tools

Package Manager: [npm, yarn, pnpm]
Build Tool: [Vite, Webpack, etc.]
Linter/Formatter: [ESLint, Prettier]
Testing: [Jest, Vitest, etc.]

Key Files & Directories
/src
  /components  - [Description]
  /utils       - [Description]
  /services    - [Description]
  /types       - [Description]
Development Workflow

[How to start dev server]
[How to run tests]
[How to build for production]
[Branch naming conventions]

Important Notes

[Any quirks or gotchas]
[Performance considerations]
[Security requirements]
[Browser/platform support]

Current Focus

[Setting up Databases]
[Known issues or tech debt]
[Upcoming features]

Preferences

[Your coding preferences]
[How you like explanations]
[Preferred libraries/approaches]
