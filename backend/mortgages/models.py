from django.db import models


class Banks(models.Model):
    bank_name = models.CharField(max_length=150, db_index=True, unique=True, blank=False, verbose_name='Название Банка')
    bank_logo = models.ImageField(upload_to='logo_bank/', null=True, blank=True)
    preference_is_active = models.BooleanField(default=False, verbose_name='Преференция, Есть/нет ')
    preference_value = models.FloatField(null=True, blank=True, verbose_name='Сколько %')
    preference_comment = models.CharField(max_length=255, blank=True, verbose_name='Комментарий к преференции')

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'
        ordering = ['bank_name']


class TargetCredits(models.Model):
    target_name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Название цели программы')
    target_desc = models.CharField(max_length=255, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.target_name

    class Meta:
        verbose_name = 'Цель программы'
        verbose_name_plural = 'Цели программ'
        ordering = ['target_name']


class MortgagePrograms(models.Model):
    programs_bank = models.ForeignKey(Banks, on_delete=models.CASCADE, verbose_name='Название Банка', blank=False)
    programs_target = models.ManyToManyField(TargetCredits, verbose_name='Цель программы', blank=False)
    programs_name = models.CharField(max_length=150, db_index=True, verbose_name='Название ипотечной программы')
    rate = models.FloatField(db_index=True, blank=False, verbose_name='Ставка')
    rate_salary = models.FloatField(db_index=True, null=True, blank=True, verbose_name='Ставка, для зарплатников')
    first_payment = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Первоначальный взнос')
    min_sum_credit = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Минимальная сумма кредита, руб')
    max_sum_credit = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Максимальная сумма кредита, руб')
    min_time_credit = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Минимальный срок кредита, лет')
    max_time_credit = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Максимальный срок кредита, лет')
    min_borrower_age = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Минимальный возраст заёмщика')
    max_borrower_age = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='Максимальный возраст заёмщика')

    understatement_is_active = models.BooleanField(default=False, verbose_name='Занижение, Есть/нет')
    understatement_comment = models.CharField(max_length=255, blank=True, verbose_name='Комментарий к занижению')
    co_borrowers = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Созаемщики')
    commission = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Коммисия')
    seller_registration = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Регистрация продавца')

    ANSWER_CHOICES = (
        ('yes', 'Да'),
        ('no', 'Нет')
    )

    express_issue = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Экспресс выдача')
    inclusion_children = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Включение детей в число собственников')

    room = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Комната')
    room_comment = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Комментарий к Комната')
    share = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Доля')
    share_comment = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Комментарий к Доля')
    private_house = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Частный дом')
    private_comment = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Комментарий к Частный дом')
    apartments = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Апартаменты')
    apartments_comment = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Комментарий к Апартаменты')
    redevelopment = models.CharField(choices=ANSWER_CHOICES, max_length=255, db_index=True, blank=True, verbose_name='Перепланировка')
    redevelopment_comment = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Комментарий к Перепланировка')

    overlap = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Перекрытия')
    storeys = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Этажность')
    housing_wear = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Износ жилья')
    req_tech_docs = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Требования к техническим документам')
    add_info = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Дополнительная информация')

    def __str__(self):
        return self.programs_name

    class Meta:
        verbose_name = 'Программа по ипотеке'
        verbose_name_plural = 'Программы по ипотеке'
        ordering = ['programs_bank']
