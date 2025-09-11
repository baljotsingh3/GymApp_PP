
# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from Blog.models import Blog
from Blog.forms import BlogForm



def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs})


def member_personal_blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/member_personal_blog_detail.html', {'blog': blog})

@login_required
def blog_create(request):
    member = request.user.groups.filter(name="Member").exists() 
    trainer = request.user.groups.filter(name="Trainer").exists()
    print("Member: ",member, "Trainer:" , trainer)
    if member:
        user_role = 'Member'
    elif trainer:
        user_role = 'Trainer'
    else:
        return redirect('gymApp:home')  # Use 'return' here to ensure redirect happens

    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('Blog:blog_list')
    else:
        form = BlogForm()

    context = {
        'form': form,
        'user_role': user_role,   # Pass this to template
    }
    return render(request, 'blog/blog_form.html', context)

# 
@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    # Check if the current user is the author
    if blog.author != request.user:
        return redirect('Blog:blog_list')
    
    # Determine user role (same as in blog_create)
    member = request.user.groups.filter(name="Member").exists()
    trainer = request.user.groups.filter(name="Trainer").exists()
    print("Member: ", member, "Trainer:", trainer)
    
    if member:
        user_role = 'Member'
    elif trainer:
        user_role = 'Trainer'
    else:
        return redirect('gymApp:home')
    
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('Blog:blog_detail', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    
    context = {
        'form': form,
        'user_role': user_role,   # Pass this to template
    }
    return render(request, 'blog/blog_form.html', context)



@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author == request.user:
        blog.delete()
    return redirect('Blog:blog_list')
