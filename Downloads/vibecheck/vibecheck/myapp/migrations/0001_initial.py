from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="FAQ", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ("category", models.CharField(max_length=50)), ("question", models.CharField(max_length=255)),
            ("answer", models.TextField())]),
        migrations.CreateModel(name="ErrorCode", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ("code", models.IntegerField(unique=True)), ("title", models.CharField(max_length=100)),
            ("explanation", models.TextField()), ("fix", models.TextField())], options={"ordering": ["code"]}),
        migrations.CreateModel(name="Ticket", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
            ("name", models.CharField(blank=True, max_length=100)), ("email", models.EmailField(blank=True, max_length=254)),
            ("subject", models.CharField(max_length=150)), ("message", models.TextField()),
            ("source", models.CharField(default="form", max_length=20)), ("status", models.CharField(default="open", max_length=20)),
            ("created", models.DateTimeField(auto_now_add=True))], options={"ordering": ["-created"]}),
    ]
