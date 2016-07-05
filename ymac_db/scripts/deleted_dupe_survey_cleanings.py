for row in SurveyCleaning.objects.all():
    matched = SurveyCleaning.objects.filter(data_path=row.data_path)
    if matched.count() > 1:
        for sc in matched:
            if sc.heritagesurvey_set.all() == row.heritagesurvey_set.all():
                print(row)
