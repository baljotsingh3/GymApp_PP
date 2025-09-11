from django.contrib.auth.mixins import UserPassesTestMixin



class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None  # override in subclass

    def test_func(self):
        return self.request.user.groups.filter(name=self.group_required).exists()




