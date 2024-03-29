from django.shortcuts import render


# Handle 404, 500, 400, 403
def handler404(request, *args, **argv):
    return render(request, '404.html', {}, status=404)  


def handler500(request, *args, **argv):
    return render(request, '500.html', {}, status=500)


def handler400(request, *args, **argv):
    return render(request, '400.html', {}, status=400)


def handler403(request, *args, **argv):
    return render(request, '403.html', {}, status=403)