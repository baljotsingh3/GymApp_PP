from rest_framework.permissions import BasePermission



class IsTrainer(BasePermission):
    """
    Allows access only to users in the Trainer group.
    """

    def has_permission(self, request, view):
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        print("Groups:", request.user.groups.values_list("name", flat=True))
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Trainer").exists()
        )
        
        
class IsMember(BasePermission):
    """
    Allows access only to users in the Trainer group.
    """

    def has_permission(self, request, view):
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        print("Groups:", request.user.groups.values_list("name", flat=True))
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Member").exists()
        )
        
class IsTrainerOrMember(BasePermission):
    """
    Allow access if the user is either a Trainer or a Member.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and (
                request.user.groups.filter(name="Trainer").exists()
                or request.user.groups.filter(name="Member").exists()
            )
        )