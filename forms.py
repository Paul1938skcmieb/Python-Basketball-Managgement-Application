from django.forms import ModelForm
from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Player, Coach, Payment


class PlayerForm(ModelForm):

    email = forms.EmailField(max_length=255, required=True)
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=8)
    age = forms.IntegerField(min_value=0)
    nationality = CountryField()
    position = forms.ChoiceField(choices=Player.POSITION_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label='Confirm password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    class Meta:
        model = Player
        fields = ('username', 'email', 'name', 'phone', 'age',
                  'nationality', 'position', 'password', 'confirm_password')

    def save(self, commit=True):
        player = super(PlayerForm, self).save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            is_active=False
        )

        player.user = user
        if commit:
            user.save()
            player.save()

        return player


class CoachForm(ModelForm):

    email = forms.EmailField(max_length=255, required=True)
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=8)
    age = forms.IntegerField(min_value=0)
    nationality = CountryField()
    position = forms.ChoiceField(choices=Coach.POSITION_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label='Confirm password')

    class Meta:
        model = Coach
        fields = ('username', 'email', 'name', 'phone', 'age',
                  'nationality', 'position', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        coach = super(CoachForm, self).save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            is_active=False
        )
        coach.user = user
        if commit:
            user.save()
            coach.save()

        return coach


class CoachUpdateForm(ModelForm):

    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=8)
    age = forms.IntegerField(min_value=0)
    nationality = CountryField()
    position = forms.ChoiceField(choices=Coach.POSITION_CHOICES)

    class Meta:
        model = Coach
        fields = ('name', 'phone', 'age',
                  'nationality', 'position')


class PlayerUpdateForm(ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'phone', 'age', 'nationality', 'position', 'salary', 'games_played', 'points_per_game', 'rebounds_per_game', 'assists_per_game', 'steals_per_game',
                  'blocks_per_game', 'fieldgoals_percentage', 'three_point_percentage', 'free_throw_percentage')

    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=8)
    age = forms.IntegerField(min_value=0)
    nationality = CountryField()
    position = forms.ChoiceField(choices=Player.POSITION_CHOICES)
    salary = forms.IntegerField(min_value=0)

    games_played = forms.FloatField(min_value=0)
    points_per_game = forms.FloatField(min_value=0)
    rebounds_per_game = forms.FloatField(min_value=0)
    assists_per_game = forms.FloatField(min_value=0)
    steals_per_game = forms.FloatField(min_value=0)
    blocks_per_game = forms.FloatField(min_value=0)

    fieldgoals_percentage = forms.FloatField(min_value=0, max_value=100)
    three_point_percentage = forms.FloatField(min_value=0, max_value=100)
    free_throw_percentage = forms.FloatField(min_value=0, max_value=100)


class StatFilter(forms.Form):
    STAT_CHOICE = [('', 'Any'), ('points_per_game', 'Point/game'), ('rebounds_per_game', 'Rebounds/game'), ('assists_per_game', 'Assists/game'),
                   ('steals_per_game', 'Steals/game'), ('blocks_per_game', 'Blocks/game'), ('fieldgoals_percentage',
                                                                                            'FG%'), ('three_point_percentage', '3P%'), ('free_throw_percentage', 'FT%')
                   ]
    stat = forms.ChoiceField(choices=STAT_CHOICE, required=False)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'player', 'coach')
    amount = forms.IntegerField(min_value=0, max_value=100000)

    def clean(self):
        cleaned_data = super().clean()
        player = cleaned_data.get('player')
        coach = cleaned_data.get('coach')
        if coach and player:
            raise forms.ValidationError(
                "You can only make a payment to one person.")
