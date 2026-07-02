from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=50, unique=True, verbose_name='Название статуса'
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class OperationType(models.Model):
    name = models.CharField(
        max_length=50, unique=True, verbose_name='Название типа'
    )

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=50, unique=True, verbose_name='Название категории'
    )
    type = models.ForeignKey(
        OperationType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.type.name})'


class Subcategory(models.Model):
    name = models.CharField(
        max_length=50, unique=True, verbose_name='Название подкатегории'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.name} ({self.category.name})'
