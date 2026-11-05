# CourseHub — Architecture & Design

> **Status:** Draft — skeleton only. Content to be agreed in the Sprint 1 design session.
>
> **Task:** `AB#TBD`
> **Branch:** `team-a/design-task` → `team-a/sprint-1`
> **Owner:** Team A
> **Last updated:** _TBD_

## Context and fixed decisions (given)

- One custom user model: `accounts.User`, based on `AbstractUser`, with a `role` field (`STUDENT` or `INSTRUCTOR`). It is already on `team-a/sprint-1`. No separate Student or Instructor user tables.

---

## 1. Entity relationship diagram (ERD)

**Required entities:** `User`, `Course`, `Module`, `Lesson`, `Enrollment`, `LessonProgress`, `Review`.

- Diagram (draw.io link or whiteboard photo): _TBD_
- Source file (for example `docs/erd.drawio`): _TBD_
- How to open/edit the diagram: _TBD_

### Keys and relationships

| Entity | Primary key | Foreign keys | Relationship / cardinality | Notes |
|---|---|---|---|---|
| `User` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| `Course` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| `Module` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| `Lesson` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| `Enrollment` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| `LessonProgress` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| `Review` | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

### Relationship notes

- One-to-many: _TBD_
- Many-to-many: _TBD_
- Unique constraints: _TBD_
- Delete behaviour: _TBD_

---

## 2. Django apps and ownership

| App | Responsibility | Owner | Status |
|---|---|---|---|
| _TBD_ | _TBD_ | _TBD_ | _TBD_ |

### App boundaries and dependencies

- Dependency direction: _TBD_
- What each app must not own: _TBD_
- Shared code / utilities: _TBD_

---

## 3. URL and permission table

Access levels: **Public**, **Student-only**, **Instructor-only**.

| URL | Page / purpose | View | Access level | Login required | Notes |
|---|---|---|---|---|---|
| _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

### Permission rules

- Guest behaviour (302 to login vs 403): _TBD_
- Student behaviour on instructor-only pages: _TBD_
- Instructor behaviour on student-only pages: _TBD_
- Where enforcement lives (decorator, mixin, view, template): _TBD_

---

## 4. Conventions

### Naming

- Apps: _TBD_
- Models: _TBD_
- Views and URLs: _TBD_
- Templates: _TBD_
- Tests: _TBD_
- Branches and commits (see `CONTRIBUTING.md`): _TBD_

### Templates

- Project-level template directory: _TBD_
- App-level template directory: _TBD_
- Naming pattern (`<app>/<page>.html`): _TBD_
- Shared partials: _TBD_

### Static files

- CSS / JS / images location: _TBD_
- Static URL and collection: _TBD_
- Third-party assets (CDN vs vendored): _TBD_

---

## 5. Sprint 1 in detail

### Goal

_TBD_

### Scope

- In scope: _TBD_
- Out of scope: _TBD_

### Deliverables

- _TBD_

### Definition of Done

- _TBD_

### Task split

| Task | Task number | Owner | Depends on | Definition of Done |
|---|---|---|---|---|
| _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

---

## 6. Sprints 2–4 (rough sketch)

### Sprint 2

- Theme: _TBD_
- Main features: _TBD_
- Models touched: _TBD_
- Risks: _TBD_

### Sprint 3

- Theme: _TBD_
- Main features: _TBD_
- Models touched: _TBD_
- Risks: _TBD_

### Sprint 4

- Theme: _TBD_
- Main features: _TBD_
- Models touched: _TBD_
- Risks: _TBD_

---

## Decisions log

| Date | Decision | Rationale | Agreed by |
|---|---|---|---|
| _TBD_ | _TBD_ | _TBD_ | _TBD_ |

## Open questions

- _TBD_

## Group sign-off

| Name | Role | Agreed |
|---|---|---|
| _TBD_ | _TBD_ | _TBD_ |
