from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from polls.models import Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    request.toolbar.populate()
    menu = request.toolbar.get_or_create_menu('polls-app', _('Polls'))
    menu.add_modal_item(_('Change this Poll'), url=reverse('admin:polls_poll_change', args=[poll_id]))
    menu.add_sideframe_item(_('Show History of this Poll'), url=reverse('admin:polls_poll_history', args=[poll_id]))
    menu.add_sideframe_item(_('Delete this Poll'), url=reverse('admin:polls_poll_delete', args=[poll_id]))

    return render(request, 'polls/detail.html', {'poll': poll})
