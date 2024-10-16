from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name=None, email=None, **extra_fields):
        if not (email or first_name):
            raise ValueError("Укажите email")
        if email:
            email = self.normalize_email(email)

        user = self.model(first_name=first_name, **extra_fields)
        if email:
            user.email = email
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, **extra_fields):
        return self._create_user(first_name, email, last_name=last_name, **extra_fields)
