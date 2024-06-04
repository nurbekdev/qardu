from celery import shared_task
from django.db.models import Case, IntegerField, Q, Sum, When

from oauth.models import Teacher
from posts.models import AcademicYear


@shared_task
def status_points_teachers():
    academic_years = AcademicYear.objects.prefetch_related("academic_points").all()
    for academic_year in academic_years:
        # Fetch and annotate teachers with total points in the given academic year period
        teachers = Teacher.objects.filter(department__isnull=False).annotate(
            points=Sum(
                Case(
                    When(
                        Q(post__date__gte=academic_year.from_date)
                        & Q(
                            post__date__lte=Case(
                                When(ext_date__isnull=False, then="ext_date"),
                                default=academic_year.to_date,
                            )
                        ),
                        then="post__category__coefficient",
                    ),
                    default=0,
                    output_field=IntegerField(),
                )
            )
        )

        # Initialize point counts
        academic_year.academic_points.lt_55 = 0
        academic_year.academic_points.lt_100 = 0
        academic_year.academic_points.lt_150 = 0
        academic_year.academic_points.gt_150 = 0

        for teacher in teachers:
            if teacher.points < 55:
                academic_year.academic_points.lt_55 += 1
            elif 55 <= teacher.points < 100:
                academic_year.academic_points.lt_100 += 1
            elif 100 <= teacher.points < 150:
                academic_year.academic_points.lt_150 += 1
            elif teacher.points >= 150:
                academic_year.academic_points.gt_150 += 1

        academic_year.academic_points.save()
