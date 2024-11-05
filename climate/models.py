from django.db import models

# Irrigation Field Model
class Field(models.Model):
    size = models.FloatField()
    location = models.CharField(max_length=255)
    crop_type = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Field {self.id} - {self.location}"


# Irrigation Plan Model
class IrrigationPlan(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    water_amount = models.FloatField()
    irrigation_date = models.DateTimeField()

    def __str__(self):
        return f"Irrigation Plan for Field {self.field.id} on {self.irrigation_date}"

# Crop Model
class Crop(models.Model):
    name = models.CharField(max_length=100)
    water_requirement = models.FloatField()

    def __str__(self):
        return self.name

# Water Source Model
class WaterSource(models.Model):
    type = models.CharField(max_length=100)
    capacity = models.FloatField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Water Source {self.type} - {self.location}"

# Weather Data Model
class WeatherData(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    rainfall = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return f"Weather on {self.date} - Temp: {self.temperature}°C"


# Irrigation System Model
class IrrigationSystem(models.Model):
    SYSTEM_TYPES = [
        ('drip', 'Goutte à goutte'),
        ('sprinkler', 'Aspersion'),
        ('surface', 'Surface'),
        ('subsurface', 'Subsurface'),
    ]

    type = models.CharField(max_length=50, choices=SYSTEM_TYPES)
    efficiency = models.FloatField(help_text="Efficacité du système en pourcentage")
    installation_date = models.DateField()
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_type_display()} System for Field {self.field.id}"

#FertilizationSchedule model 
class FertilizationSchedule(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    fertilizer_type = models.CharField(max_length=100)
    amount = models.FloatField()  # en kg/hectare, par exemple
    application_date = models.DateField()

    def __str__(self):
        return f"{self.fertilizer_type} pour {self.crop.name} le {self.application_date}"

# Water Usage Model
class WaterUsage(models.Model):
    irrigation_plan = models.ForeignKey(IrrigationPlan, on_delete=models.CASCADE)
    water_source = models.ForeignKey(WaterSource, on_delete=models.CASCADE)
    amount_used = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount_used} liters from {self.water_source} using {self.irrigation_plan}"


class Machine(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    purchase_date = models.DateField()
    last_maintenance_date = models.DateField(null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - Field {self.field.id if self.field else 'None'}"