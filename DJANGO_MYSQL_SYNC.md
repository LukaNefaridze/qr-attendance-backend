# Django Admin ↔ MySQL Workbench Synchronization

## Quick Answer: **YES, changes are automatic!**

When you make changes in Django Admin, they are **immediately saved** to the MySQL database. MySQL Workbench will show these changes (you may need to refresh).

## How It Works

```
Django Admin Interface
        ↓
   Django ORM
        ↓
   MySQL Database (attendance_db)
        ↓
   MySQL Workbench (reads same database)
```

## Data Flow

### Creating/Editing in Django Admin:
1. You fill out a form in Django Admin (e.g., add a new User)
2. Click "Save"
3. Django executes: `INSERT INTO core_user ...` or `UPDATE core_user SET ...`
4. Data is **immediately** written to MySQL
5. MySQL Workbench can see it (refresh if needed)

### Viewing in MySQL Workbench:
1. Open MySQL Workbench
2. Connect to `attendance_db`
3. Browse tables (e.g., `core_user`, `core_course`, `core_enrollment`)
4. **Refresh** the table view to see latest changes
5. All Django Admin changes will be visible

## Table Names in MySQL

Django creates tables with the format: `{app_name}_{model_name}`

| Django Model | MySQL Table Name |
|-------------|------------------|
| User | `core_user` |
| Course | `core_course` |
| Enrollment | `core_enrollment` |
| Timetable | `core_timetable` |
| Session | `core_session` |
| Attendance | `core_attendance` |

## Two-Way Editing

### ✅ Safe: Editing in Django Admin
- Django validates data
- Respects model constraints
- Handles relationships correctly
- **Recommended approach**

### ⚠️ Caution: Direct MySQL Editing
- You can edit directly in MySQL Workbench
- Changes will appear in Django Admin
- **BUT**: Django won't validate the data
- May break relationships or constraints
- Use with caution!

## Example Workflow

### Adding a User via Django Admin:
1. Go to: `http://127.0.0.1:8000/admin/core/user/add/`
2. Fill in: username, email, password
3. Check: `is_student` or `is_professor`
4. Click: "Save"
5. **Immediately** check MySQL Workbench:
   ```sql
   SELECT * FROM core_user WHERE username = 'newuser';
   ```
   → The user will be there!

### Assigning Student to Course (Enrollment):
1. Django Admin → Enrollments → Add Enrollment
2. Select: Student and Course
3. Click: "Save"
4. Check MySQL Workbench:
   ```sql
   SELECT * FROM core_enrollment;
   ```
   → The enrollment will be there!

## Tips

1. **Always refresh** MySQL Workbench after making Django Admin changes
2. **Use Django Admin** for data entry (it's safer and validates data)
3. **Use MySQL Workbench** for viewing/querying data
4. Both tools access the **same database** - no sync needed!

## Troubleshooting

**Q: I made changes in Django Admin but don't see them in MySQL Workbench**
- **A**: Refresh the table view in MySQL Workbench (right-click → Refresh All)

**Q: Can I edit data directly in MySQL Workbench?**
- **A**: Yes, but Django won't validate it. Use Django Admin when possible.

**Q: Will changes in MySQL Workbench show in Django Admin?**
- **A**: Yes, refresh the Django Admin page to see them.

**Q: Are there any delays?**
- **A**: No, changes are immediate. Both tools read/write to the same database.

