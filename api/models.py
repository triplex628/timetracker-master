from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

import datetime

from django.core.exceptions import ValidationError
from datetime import timedelta

def check_daily_work_hours(task):
    user_tasks_today = TaskModel.objects.filter(
        employee=task.employee,
        start_time__date=timezone.now().date()
    )
    
    total_duration_today = sum([
        task.duration for task in user_tasks_today
    ], timedelta())
    
    if total_duration_today + task.duration > timedelta(hours=8):
        raise ValidationError("Рабочее время на сегодня превышено (8 часов)")

class AdminModel(AbstractUser):
    max_length = 255
    password_length = 20

  
    name = models.CharField(max_length=max_length, verbose_name="Имя")
    surname = models.CharField(max_length=max_length, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=max_length, verbose_name="Отчество", null=True, blank=True, default='')

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic} ({self.username})"
    
    def save(self, *args, **kwargs):
        if not self.patronymic:
            self.patronymic = ""
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["surname", "name", "patronymic"]
        verbose_name_plural = "Администраторы"


class ItemModel(models.Model):
    max_length = 1000
    short_max_length = 255

    TYPES_OF_WORK = [
        ("Сейсморазведка", "Сейсморазведка"),
        ("Вспомогательное оборудование", "Вспомогательное оборудование"),
        ("Электроразведка", "Электроразведка"),
        ("Магниторазведка", "Магниторазведка"),
        ("Радиометрия", "Радиометрия"),
        ("Нестандартные изделия", "Нестандартные изделия"),
    ]

    SUBTYPES_OF_WORK = (
#   Сейсморазведка
        ("Сейсмостанция, используемая с комплектом", "Сейсмостанция, используемая с комплектом"),
        ("Накопители", "Накопители"),
        ("Источники", "Источники"),
        ("Приемники", "Приемники"),
#   Вспомогательное оборудование
        ("Палубные лебедки", "Палубные лебедки"),
        ("Скважинные лебёдки", "Скважинные лебёдки"),
        ("Палубные катушки", "Палубные катушки"),
        ("Геофизические катушки", "Геофизические катушки"),
        ("Прочее вспомогательное оборудование", "Прочее вспомогательное оборудование"),
#   Магниторазведка
        ("Акваторные магнитометры", "Акваторные магнитометры"),
        ("АЭРО магнитометры", "АЭРО магнитометры"),
        ("Наземные магнитометры", "Наземные магнитометры"),
        ("Прочее оборудование магниторазведки", "Прочее оборудование магниторазведки"),
#   Радиометрия
        ("СРП-20 сцинтилляционный радиометр", "СРП-20 сцинтилляционный радиометр"),
#   Элкектроразведка
        ("Электроразведочная станция с которой используется оборудование", "Электроразведочная станция с которой используется оборудование"),
        ("Электроразведочные комплексы", "Электроразведочные комплексы"),
        ("Усиленная герметичная коса для электротомографии каналы/кол-во разъемов", "Усиленная герметичная коса для электротомографии каналы/кол-во разъемов"),
        ("Морская электроразведочная коса", "Морская электроразведочная коса"),
        ("Прочее оборудование эектроразведки", "Прочее оборудование эектроразведки")
    )

    CATEGORY_OF_ITEM = (
    #   Сейсморазведка
        ("Акваторные накопители", "Акваторные накопители"),
        ("Скважинные накопители", "Скважинные накопители"),
        ("Акваторные источники", "Акваторные источники"),
        ("Скважинные источники", "Скважинные источники"),
        ("Наземные источники", "Наземные источники"),
        ("Акваторные приемники", "Акваторные приемники"),
        ("Скаважинные приемники", "Скаважинные приемники"),
        ("Наземные сейсмические приемники", "Наземные сейсмические приемники"),
    #   Палубные лебедки
        ("Палубные лебёдки для кос", "Палубные лебёдки для кос"),
        ("Палубные лебёдки высоковольтные", "Палубные лебёдки высоковольтные"),
    #   Палубные катушки		
        ("Палубные катушки для кос", "Палубные катушки для кос"),
        ("Палубные катушки высоковольтные", "Палубные катушки высоковольтные"),
    #   Геофизические катушки
        ("КТ-1 Универсальная геофизическая катушка", "КТ-1 Универсальная геофизическая катушка"),
        ("КТ-3C Универсальная катушка", "КТ-3C Универсальная катушка"),
        ("КТ-4C Геофизическая катушка", "КТ-4C Геофизическая катушка"),
        ("КТ-5C Геофизическая катушка", "КТ-5C Геофизическая катушка"),
    #   Прочее оборудование эектроразведки
        ("Антенны (магнитные датчики ARMT-5)", "Антенны (магнитные датчики ARMT-5)"),
        ("Коммутаторы", "Коммутаторы"),
        ("Удлинители, коннектора, соединители", "Удлинители, коннектора, соединители"),
        ("Электроды", "Электроды"),
        ("Сумки, ящики", "Сумки, ящики"),
    )

    SUBCATEGORY_OF_ITEM = (
        ("Морские электроискровые источники SWS и VSWS", "Морские электроискровые источники SWS и VSWS"),
        ("Пресноводные электроискровые источники FWS", "Вспомогательное оборудование"),
        ("Заглубляемые электроискровые источники DWS", "Заглубляемые электроискровые источники DWS"),
        ("Электродинамические источники G-Boomer", "Электродинамические источники G-Boomer"),
        ("Высоковольтная коаксиальная кабельная линия источника плавающая", "Высоковольтная коаксиальная кабельная линия источника плавающая"),
        ("Высоковольтная коаксиальная кабельная линия источника палубная", "Высоковольтная коаксиальная кабельная линия источника палубная"),
        ("Электроискровой скважинный источник", "Электроискровой скважинный источник"),
        ("Элекродинамический скважинный источник", "Элекродинамический скважинный источник"),
        ("Механизированниые молоты", "Механизированниые молоты"),
        ("Кувалды", "Кувалды"),
        ("Сейсморужья", "Сейсморужья"),
        ("WellStreamer Гидрофонная коса", "WellStreamer Гидрофонная коса"),
        ("GStreamer 3С скважиннный сейсмический  зонд", "GStreamer 3С скважиннный сейсмический  зонд"),
        ("GStreamer-E скважинный 3С сейсмический зонд с механизированным прижимом", "GStreamer-E скважинный 3С сейсмический зонд с механизированным прижимом"),
        ("GStreamer-P скважинный 3С сейсмический зонд с пневмоприжимом", "GStreamer-P скважинный 3С сейсмический зонд с пневмоприжимом"),
    )

    
    title = models.CharField(max_length=max_length, verbose_name='Название прибора')
    seria = models.CharField(max_length=short_max_length, verbose_name='Серия прибора', null=True, blank=True)
    types_of_work = models.CharField(max_length=max_length, choices=TYPES_OF_WORK, verbose_name="Тип работы", null=True, blank=True)
    subtypes_of_work = models.CharField(max_length=max_length, choices=SUBTYPES_OF_WORK, verbose_name="Подтип работы", null=True, blank=True)
    category_of_item = models.CharField(max_length=max_length, choices=CATEGORY_OF_ITEM, verbose_name="Категория прибора", null=True, blank=True)
    subcategory_of_item = models.CharField(max_length=max_length, choices=SUBCATEGORY_OF_ITEM, verbose_name="Подкатегория прибора", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Детали"


class PlotModel(models.Model):
    max_length = 255
    title = models.CharField(verbose_name="Название", max_length=max_length)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Участки"


class TaskModel(models.Model):
    max_length = 255

    TYPE_OF_TASKS = (
        ("batch_production", "Производство"),
        ("testing", "Тестирование"),
        ("repair", "Ремонт"),
        ("shipments", "Отгрузка"),
        ("other", "Прочее")
    )
   
    title = models.CharField(max_length=max_length, verbose_name="Название")
    admin_comment = models.TextField(verbose_name="Комментарий администратора", null=True, blank=True)
    type_of_task = models.CharField(max_length=max_length, choices=TYPE_OF_TASKS, verbose_name="Тип работы")
    
    plot = models.ForeignKey(PlotModel, verbose_name='Участок', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, verbose_name="Прибор", null=True, on_delete=models.CASCADE)
    manual_item_id = models.IntegerField(verbose_name="ID прибора", null=True, blank=True)
    is_available = models.BooleanField(verbose_name='Статус задачи', default=True, blank=True)
    admin    = models.ForeignKey(AdminModel, verbose_name="Администратор",null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Проверяем, если вручную введен ID прибора
        if self.manual_item_id is not None:
            try:
                # Пробуем найти прибор по вручную введенному ID
                item = ItemModel.objects.get(pk=self.manual_item_id)
                self.item = item  # Связываем найденный объект с полем item
            except ItemModel.DoesNotExist:
                raise ValueError(f"Прибор с ID {self.manual_item_id} не существует.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Задачи"


class EmployeeModel(models.Model):
    max_length = 255

    name = models.CharField(max_length=max_length, verbose_name="Имя")
    surname = models.CharField(max_length=max_length, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=max_length, verbose_name="Отчество", null=True, blank=True, default='')
    plot = models.ForeignKey(PlotModel, verbose_name="Участок", on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name="Занят", default=False, blank=True)
    
    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    def save(self, *args, **kwargs):
        if not self.patronymic:
            self.patronymic = ""
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["surname", "name", "patronymic"]
        verbose_name_plural = "Работники"   


class EmployeeTaskModel(models.Model):
    
    task = models.ForeignKey(TaskModel, verbose_name="Задача", related_name="task_tracking_tasks", on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeModel, verbose_name="Работник", related_name="employee_tracking_tasks", on_delete=models.CASCADE)
    is_paused = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)
    total_time = models.DurationField(verbose_name="Суммарное время", default=datetime.timedelta(milliseconds=0))
    employee_comment = models.TextField(verbose_name="Комментарий работника", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="Время начала", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="Время окончания", null=True, blank=True)
    #item_id = models.IntegerField(verbose_name="ID прибора", null=True, blank=True)
   # admin = models.ForeignKey(AdminModel, verbose_name="ID администратора", null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.task} {self.employee}"
    
    def save(self, *args, **kwargs):
        #if self.item_id is not None:
         #   try:
          #      item = ItemModel.objects.get(pk=self.item_id)
           # except ItemModel.DoesNotExist:
            #    raise ValueError(f"Прибор с ID {self.item_id} не существует.")

        if not self.employee_comment:
            self.employee_comment = "нет комментария"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Задачи работников"


class TrackingTaskModel(models.Model):
    max_length = 255

    start_time = models.DateTimeField(verbose_name="Время начала", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="Время окончания", null=True, blank=True)
    employee_task = models.ForeignKey(EmployeeTaskModel, verbose_name="Задача работника", null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.employee_task}"

    class Meta:
        verbose_name_plural = "Отслеживаемые задачи"

    @classmethod
    def get_latest_tracking_task(cls, employee_task):
        return cls.objects.filter(employee_task=employee_task).order_by('-start_time').first()
