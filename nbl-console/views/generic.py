import os

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from cloud import forms

__all__ = (
    'FileDeleteView',
    'FileManagementView',
)


class FileManagementView(View):
    base_path = None
    template_name = None
    form = forms.FileUploadForm

    def list_files(self):
        """
        List all regular files within the base path.
        """
        return [
            name for name in os.listdir(self.base_path) if not name.startswith('__')
        ]

    def save_file(self, file, overwrite=False):
        """
        Save an uploaded file to disk.
        """
        filepath = f'{self.base_path}/{file.name}'

        # Check whether file already exists
        if os.path.isfile(filepath) and not overwrite:
            raise FileExistsError()

        with open(filepath, 'wb+') as new_file:
            for chunk in file.chunks():
                new_file.write(chunk)

    def extra_context(self, request):
        """
        Provide any additional context to include when rendering the response template.
        """
        return {}

    def get(self, request):

        return render(request, self.template_name, {
            'form': self.form(),
            **self.extra_context(request)
        })

    def post(self, request):
        form = self.form(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data['file']
            overwrite = form.cleaned_data['overwrite']
            try:
                self.save_file(file, overwrite=overwrite)
                return redirect(request.path)
            except FileExistsError:
                form.add_error('file', 'A file with this name already exists. Check "overwrite" below to replace '
                                       'it with the uploaded file.')

        return render(request, 'cloud/scripts.html', {
            'form': form,
            **self.extra_context(request)
        })


class FileDeleteView(View):
    base_path = None
    return_url = None
    template_name = 'cloud/generic/files_delete.html'
    form = forms.FileDeleteForm

    def delete_file(self, name):
        """
        Delete the specified file(s) from disk
        """
        path = os.path.join(self.base_path, name)
        os.remove(path)

    def post(self, request):
        form = self.form(self.base_path, request.POST)

        if form.is_valid() and '_confirm' in request.POST:
            for file_ in form.cleaned_data['files']:
                self.delete_file(file_)
            return redirect(reverse(self.return_url))

        return render(request, self.template_name, {
            'form': form,
            'return_url': reverse(self.return_url),
        })
