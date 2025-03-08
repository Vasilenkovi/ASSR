from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from CreateDatasetApp.models import Transaction, DatasetFile
from .utils import _apply_transaction

def versions_list(request, dataset_slug):
    dataset = get_object_or_404(DatasetFile, metadata__pk=dataset_slug)
    transactions = Transaction.objects.filter(dataset=dataset).order_by('-timestamp')
    return render(request, 'Datasets/versions.html', {
        'transactions': transactions,
        'dataset': dataset
    })

def version(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'Datasets/version-detail.html', {'transaction': transaction})

def switch_to_version(request, pk):
    if pk==-1:
        dataset.source_list.set(dataset.ancestor_list.all())
        dataset.currentFile = dataset.ancestorFile
        dataset.save()
        return redirect('dataset:view_dataset', dataset_slug=dataset.metadata.pk)
    target_transaction = get_object_or_404(Transaction, pk=pk)
    dataset = target_transaction.dataset

    try:
        dataset.source_list.set(dataset.ancestor_list.all())
        dataset.currentFile = dataset.ancestorFile
        dataset.save()

        transactions = Transaction.objects.filter(
            dataset=dataset,
            timestamp__lte=target_transaction.timestamp
        ).order_by('timestamp')

        for transaction in transactions:
            _apply_transaction(transaction, dataset, save_transaction=False)

        return redirect('dataset:view_dataset', dataset_slug=dataset.metadata.pk)

    except Exception as e:
        return HttpResponse(f"Ошибка восстановления: {str(e)}", status=500)
    
def switch_to_init_version(request, dataset_slug):
    dataset = get_object_or_404(DatasetFile, metadata__pk=dataset_slug)
    try:

        dataset.source_list.set(dataset.ancestor_list.all())
        dataset.currentFile = dataset.ancestorFile
        dataset.save()
        return redirect('dataset:view_dataset', dataset_slug=dataset_slug)
        
    except Exception as e:
        return HttpResponse(f"Ошибка восстановления: {str(e)}", status=500)