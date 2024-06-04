from datetime import date

import xlsxwriter
from django.db.models import Q, Sum

from category.models import Category
from oauth.models import Teacher


def create_workbook(filename, title):
    """
    Create a new Excel workbook and add a worksheet.
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(title)
    return workbook, worksheet


def set_standard_formats(workbook):
    """
    Set standard formats for the workbook.
    """
    merge_format = workbook.add_format(
        {
            "bold": True,
            "align": "center",
            "border": 1,
            "valign": "vcenter",
            "text_wrap": True,
            "bg_color": "#dbd9d9",
        }
    )
    text_format = workbook.add_format(
        {"align": "center", "valign": "vcenter", "text_wrap": True}
    )
    return merge_format, text_format


def excel_writer(from_date, to_date):
    workbook, worksheet = create_workbook(
        f"media/analysis_{from_date}-{to_date}.xlsx", "analysis"
    )
    merge_format, text_format = set_standard_formats(workbook)

    column = [chr(i) for i in range(ord("B"), ord("Z") + 1)] + [
        f"A{i}" for i in range(ord("A"), ord("Z") + 1)
    ]

    worksheet.set_column("A:A", 40)
    worksheet.write("A1", "Наименование", merge_format)
    setup_columns(worksheet, from_date, to_date, column, merge_format)

    categories = Category.objects.all()
    for row, category in enumerate(categories, start=3):
        worksheet.write(f"A{row}", category.name, merge_format)
        fill_category_data(
            worksheet, category, from_date, to_date, column, text_format, row
        )

    workbook.close()
    return workbook


def setup_columns(worksheet, from_date, to_date, column, merge_format):
    for i, year in enumerate(range(from_date, to_date)):
        print(i, year)
        col_index = 2 * i
        worksheet.merge_range(
            f"{column[col_index]}1:{column[col_index + 1]}1",
            f"{year}-{year + 1}",
            merge_format,
        )
        worksheet.write(f"{column[col_index]}2", "Кол-во", merge_format)
        worksheet.write(f"{column[col_index + 1]}2", "Баллы", merge_format)


def fill_category_data(
    worksheet, category, from_date, to_date, column, text_format, row
):
    for i, year in enumerate(range(from_date, to_date)):
        from_academic_date = date(year, 9, 1)
        to_academic_date = date(year + 1, 8, 31)
        post_count = (
            category.post_set.filter(date__range=(from_academic_date, to_academic_date))
            .distinct()
            .count()
        )
        total_sum = round(category.coefficient * post_count, 2)
        col_index = 2 * i
        worksheet.write(f"{column[col_index]}{row}", post_count, text_format)
        worksheet.write(f"{column[col_index + 1]}{row}", total_sum, text_format)


def excel_teachers(
    years, start_date, end_date, department, name, uuid, level, order_by
):
    filename = f"media/analysis_teachers_{years}.xlsx"
    workbook, worksheet = create_workbook(filename, "analysis")
    merge_format, text_format = set_standard_formats(workbook)

    setup_teacher_columns(worksheet, merge_format)
    teachers = get_filtered_teachers(
        start_date, end_date, department, name, uuid, level, order_by
    )
    fill_teacher_data(worksheet, teachers, text_format)

    workbook.close()
    return workbook


def setup_teacher_columns(worksheet, merge_format):
    columns = [
        "#",
        "ID",
        "Ф.И.О",
        "Кафедра",
        "Статус",
        "Дата регистрации",
        "Кол-во",
        "Баллы",
    ]
    worksheet.set_column("A:H", [4, 10, 40, 25, 15, 15, 5, 10])  # Set column widths
    worksheet.merge_range("A1:H1", "Analysis", merge_format)
    for col, title in enumerate(columns, start=2):
        worksheet.write(f"{chr(64 + col)}2", title, merge_format)


def get_filtered_teachers(
    start_date, end_date, department, name, uuid, level, order_by
):
    teachers = Teacher.objects.all()
    query = Q(post__date__gte=start_date) & Q(post__date__lte=end_date) | Q(
        post__category__id=29
    )
    teachers = teachers.filter(query).distinct()

    if department:
        teachers = teachers.filter(department=department)
    if uuid:
        teachers = teachers.filter(uuid=uuid)
    if level:
        teachers = teachers.filter(level=level)
    if name:
        teachers = teachers.filter(
            Q(first_name__icontains=name)
            | Q(last_name__icontains=name)
            | Q(father_name__icontains=name)
        )

    if order_by == "points_asc":
        teachers = teachers.annotate(
            total_points=Sum("post__category__coefficient")
        ).order_by("total_points")
    elif order_by == "points_desc":
        teachers = teachers.annotate(
            total_points=Sum("post__category__coefficient")
        ).order_by("-total_points")
    else:
        teachers = teachers.annotate(
            total_points=Sum("post__category__coefficient")
        ).order_by("last_name", "first_name", "father_name", "-total_points")

    return teachers


def fill_teacher_data(worksheet, teachers, text_format):
    for row, teacher in enumerate(teachers, start=3):
        post_count = (
            teacher.post_set.filter(
                Q(date__gte=teacher.post__date__gte)
                & Q(date__lte=teacher.post__date__lte)
                | Q(category__id=29)
            )
            .distinct()
            .count()
        )

        values = [
            row - 2,  # Index
            teacher.uuid,
            teacher.get_full_name(),
            teacher.department.name if teacher.department else "N/A",
            teacher.get_status_display(),
            teacher.created.date(),
            post_count,
            teacher.total_points,
        ]

        for col, value in enumerate(values, start=1):
            worksheet.write(f"{chr(64 + col)}{row}", value, text_format)
