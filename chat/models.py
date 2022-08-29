from django.db import models

# Create your models here.

class ChatDialog(models.Model):
    start_date = models.DateTimeField('Дата создания', auto_now=True)
    is_active = models.BooleanField('Активность', default=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='пользователь',
                               related_name='user_dialogs', default='1')

    def __str__(self):
        return f'{self.start_date}'

    def check_active(self):
        return self.ratings.count()

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'


class ChatMessage(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='пользователь',
                               related_name='user_messages')
    dialog = models.ForeignKey(ChatDialog, on_delete=models.CASCADE, verbose_name='диалог',
                               related_name='dialog_messages')
    create_at = models.DateTimeField('Дата', auto_now=True)
    body = models.TextField('Текст обращения')

    def __str__(self):
        return f'{self.user} - {self.body} - {self.dialog}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

