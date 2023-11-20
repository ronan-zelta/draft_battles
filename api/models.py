from django.db import models

class NFLPlayer(models.Model):
    uid = models.CharField(max_length=8, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    pos = models.CharField(max_length=3, verbose_name='Position')
    years_played = models.CharField(max_length=11, blank=True, null=True)
    img = models.CharField(max_length=100, null=True, blank=True)
    name_searchable = models.CharField(max_length=255, default="")
    
    # Fantasy points fields
    fp_2022 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2021 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2020 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2019 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2018 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2017 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2016 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2015 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2014 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2013 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2012 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2011 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2010 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2009 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2008 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2007 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2006 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2005 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2004 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2003 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2002 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2001 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_2000 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1999 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1998 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1997 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1996 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1995 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1994 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1993 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1992 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1991 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1990 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1989 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1988 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1987 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1986 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1985 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1984 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1983 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1982 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1981 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1980 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1979 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1978 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1977 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1976 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1975 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1974 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1973 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1972 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1971 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fp_1970 = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculating years_played before saving
        years_with_points = []
        for year in range(1970, 2023):  # Adjust according to data range
            if getattr(self, f'fp_{year}') is not None:
                years_with_points.append(year)
        if years_with_points:
            self.years_played = f"({min(years_with_points)}-{max(years_with_points)})"
        super(NFLPlayer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name