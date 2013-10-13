django CMS Tutorial - Step 2
============================
During this tutorial or your experience with django itself you've probably seen the placeholders before:

```html
{% placeholder "content" %}
```

If you didn't, don't worry: Placeholders are an easy way to define sections in html code to be editable through our frontend editing. That's cool. But imagine the following situation: On your site, the footer should be editable through frontend. Sure, you could define a footer placeholder im the html template but that would mean that you'd have to insert the information on every single page you make - not so cool.

So we came up with a solution: Stacks.

Stacks
------

Stacks is an easy way to display the same content on multiple locations on your website. Stacks have a name and a placeholder attached to them. Once a stack is created and you added content to it, it will be saved globally. Even when you remove the stack you can reuse it at sometime later again.

There are 3 ways to use stacks.

### 1. Stack Template Tags	
You can use a template tag to display a placeholder in a template without the need for an actual placeholder in your models. This can be useful for:

* Footer
* Logo
* Header
* Text or content inside you app
* Text or content inside of 3rd party apps.

**Example:**

```python
{% load stack_tags %} {% stack "footer" %}
```

***Note:*** It is recommended to use stacks in your apphook apps instead of show_placeholder templatetags

### 2. Stack Plugins

You can create a stack out of plugins. You can create stacks out of plugin trees. After you created a stack this way you can insert a stack plugin and select a stack to be displayed instead of the stack plugin.

### 3. Stacks as templates

If you create stacks out of plugin tree you can paste the plugins contained in a stack as template. For example you can create a teaser plugin tree out of a multicolumn, text and picture plugin. You can then paste this template at the appropriate place and just edit the plugins instead of creating the same structure over and over.

### Let's create a footer!

But that's theory, let's implement a footer!

Since we want our footer on every single page, we should add it to our base template (`my_demo/templates/base.html`). So open it up and add `stack_tags` to the `load` tag at the top and add a new `stack` (e.g. `my_footer`) at the bottom of the html body. In the end it should look something like this:

```html
{% load cms_tags sekizai_tags menu_tags placeholder_tags stack_tags %}
<html>
    <head>
        {% render_block "css" %}
    </head>
    <body>
        {% cms_toolbar %}
        <ul>
            {% show_menu 0 100 100 100 %}
        </ul>
        {% block content %}{% endblock %}
        {% stack "my_footer" %}
        {% render_block "js" %}
    </body>
</html>
```

Save the template and go back to your browser. Change to draft and then structure mode and fill in content into your footer! After you've saved it, go check out the other pages on your websites to see that the footer appears there too!

Next up: [`step-3`](https://github.com/Chive/djangocms-tutorial/tree/step-3)

