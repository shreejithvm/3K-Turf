from .models import Turf
def common_choices(request):
    choices = {}
    try:
        choices["sport_choices"] = [c[0] for c in Turf._meta.get_field('sport').choices]
        choices["district_choices"] = [c[0] for c in Turf._meta.get_field('district').choices]
    except:
        choices["sport_choices"] = []
        choices["district_choices"] = []
    return choices
