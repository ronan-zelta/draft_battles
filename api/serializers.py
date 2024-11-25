from rest_framework import serializers
from .models import NFLPlayer

class NFLPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLPlayer
        fields = '__all__'  # Default to all fields

    def __init__(self, *args, **kwargs):
        # Remove the fantasy points data if requested
        include_fp_data = kwargs.pop('include_fp_data', True)
        super(NFLPlayerSerializer, self).__init__(*args, **kwargs)

        if not include_fp_data:
            # Exclude fantasy point fields
            excluded_fields = ['fp_' + str(year) for year in range(1970, 2024)]
            for field in excluded_fields:
                self.fields.pop(field, None)