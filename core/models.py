from django.db import models
from datetime import datetime

# Все уникальные поля, а также поля связей - индексируются Django по умолчанию


class Tractor(models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             verbose_name="ID in Omnicomm")
    serial_number = models.CharField(
        max_length=50, unique=True, verbose_name="Серийный номер"
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    # through - ссылка на промежуточную модель, которая обсепечивает связь Many2Many
    components = models.ManyToManyField(
        "Component", verbose_name="Компоненты", related_name="tractors", through="Assembly", through_fields=('tractor', 'component')
    )
    software_versions = models.ManyToManyField(
        "SoftwareVersion", verbose_name='Версии прошивок', related_name="tractors", through="Assembly", through_fields=('tractor', 'software_version')
    )

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]


class Component(models.Model):
    NAMES_CHOICES = [
        ('EN', 'ДВС'),
        ('TB', 'Коробка передач'),
        ('SC', 'Рулевая колонка'),
        ('HD', 'Гидрораспределитель'),
        ('DP', 'Дисплей'),
        ('CN', 'Контроллер'),
    ]
    designation = models.CharField(max_length=100, unique=True,
                                   verbose_name="Обозначение узла")
    verbose_name = models.CharField(
        max_length=2, choices=NAMES_CHOICES, unique=False, verbose_name="Узел")

    def __str__(self):
        return self.designation

    class Meta:
        indexes = [
            models.Index(fields=['verbose_name'])
        ]


class SoftwareVersion(models.Model):
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, verbose_name="Узел", related_name="versions")
    # Полнотекстовое обозначение ПО
    version = models.CharField(
        max_length=50, verbose_name="Обозначение ПО", blank=True, null=True
    )
    # Обозначене ПО
    tractor_model = models.CharField(
        max_length=3, verbose_name="Модель трактора", blank=True, null=True
    )
    engine_comp = models.CharField(
        max_length=3, verbose_name="Производитель ДВС", blank=True, null=True
    )
    first_number = models.PositiveSmallIntegerField(
        verbose_name="Первые цифры в названии прошивки", blank=True, null=True
    )
    second_number = models.PositiveSmallIntegerField(
        verbose_name="Вторые цифры в названии прошивки", blank=True, null=True
    )
    third_number = models.PositiveSmallIntegerField(
        verbose_name="Третие цифры в названии прошивки", blank=True, null=True
    )
    ### Вспомогательные поля ###
    # Примечание
    note = models.CharField(
        max_length=255, verbose_name="Примечание", blank=True, null=True
    )
    # Критическое обновление, все версии до него считаются неисправными
    is_critical = models.BooleanField(
        default=False, verbose_name="Критическое обновление"
    )
    # Неисправная версия
    is_broken = models.BooleanField(
        default=False, verbose_name="Неисправная версия",
    )
    # Дата выпуска ПО
    release_date = models.DateField(
        verbose_name="Дата выпуска", null=True, blank=True, default=datetime.now
    )

    class Meta:
        ordering = ['-release_date', '-version']
        constraints = [models.UniqueConstraint(
            fields=['tractor_model', 'engine_comp', 'first_number', 'second_number', 'third_number'], name='unique_version')
        ]


    def __str__(self):
        return f"{self.component.designation}: {self.version}"

class Assembly(models.Model):  # Подумать над названием
    tractor = models.ForeignKey(
        Tractor, on_delete=models.CASCADE, verbose_name="Трактор", related_name="assamblies")
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, verbose_name="Узел", related_name="assamblies")
    software_version = models.ForeignKey(
        SoftwareVersion, on_delete=models.CASCADE, verbose_name="Нынешняя версия прошивки", related_name="assamblies")

    class Meta:
        verbose_name = "Сборка"
        verbose_name_plural = "Сборки"
        constraints = [
            models.UniqueConstraint(
                fields=["tractor", "component", "software_version"], name="unique_assembly")
        ]


# class Telemetry(models.Model):
#     tractor = models.ForeignKey(
#         Tractor, on_delete=models.CASCADE, verbose_name="Трактор")
#     component = models.ForeignKey(
#         Component, on_delete=models.CASCADE, verbose_name="Узел")
#     installed_version = models.CharField(
#         max_length=20, verbose_name="Установленная версия")
#     timestamp = models.DateTimeField(
#         auto_now_add=True, verbose_name="Время получения")

#     class Meta:
#         ordering = ['-timestamp']
#         indexes = [
#             models.Index(fields=['tractor', 'component']),
#         ]

#     def __str__(self):
#         return f"{self.tractor} - {self.component}: {self.installed_version}"
