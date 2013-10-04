djangoCMS Tutorial - Step 6
===========================
During this tutorial or your experience with django itself you've probably seen the placeholders before:

```html
{% placeholder "content" %}
```

If you didn't, don't worry: Placeholders are an easy way to define sections in html code to be editable through our frontend editing. That's cool. But imaging the following situation: On your site, the footer should be editable through frontend. Sure, you could define a footer placeholder im the html template but that would mean that you'd have to insert the information on every single page you make - not so cool.

So we came up with a solution: Stacks.

Stacks
------

Stacks is an easy way to display the same content on multiple locations on your website. Stacks have a name and a placeholder attached to them. Once a stack is created and you added content to it, it will be saved globally. Even when you remove the stack you can reuse it at sometime later again.

There are 3 ways to use stacks.

### 1. Stack Template Tags	
You can use a template tag to display a placeholder in a template without the need for an actual placeholder on you models. This can be useful for:

* Footer
* Logo
* Header
* Text or content inside you app
* Text or content inside of 3th party apps.
	
**Example:**
	
```python
{% load stack_tags %} {% stack "footer" %}
```
	
***Note:*** It is recommended to use stacks in your apphook apps instead of show_placeholder templatetags

### 2. Stack Plugins

You can create a stack out of plugins. You can create stacks out of plugin trees. After you created a stack this way you can insert a stack plugin and select a stack to be displayed instead of the stack plugin.

### 3. Stacks as templates

If you create stacks out of plugin tree you can paste the plugins contained in a stack as template. For example you can create a teaser plugin tree out of a multicolumn, text and picture plugin. You can then paste this template at the appropriate place and just edit the plugins instead of creating the same structure over and over.

But that's theory, let's implement a footer!

Open up our base template `my_demo/templates/base.html` and add the following to it:

```html
{% load stack_tags %}
{% stack "my_footer" %}
```

`#TODO Save, make sure right template selected and view on site
