from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import QAUploadForm
import logging
from coolname import generate_slug
import pandas as pd
from .models import *
import datetime


# Create your views here.


def index(request):
    return render(request, "teachers/index.html")


def dashboard(request):
    return render(request, "teachers/dashboard.html")


def create_test_objective(request):
    if request.method == 'POST':
        form = QAUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info(form.cleaned_data)

            test_id = generate_slug(2)
            filestream = form.cleaned_data.get('doc')
            filestream.seek(0)
            df = pd.read_csv(filestream)
            fields = ['question_id', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'ans', 'marks']
            df = pd.DataFrame(df, columns=fields)

            for row in df.index:
                test_obj = TestObjective()
                test_obj.test_id = test_id
                test_obj.question_id = df['question_id'][row]
                test_obj.question = df['question'][row]
                test_obj.option_a = df['option_a'][row]
                test_obj.option_b = df['option_b'][row]
                test_obj.option_c = df['option_c'][row]
                test_obj.option_d = df['option_d'][row]
                test_obj.ans = df['ans'][row]
                test_obj.marks = df['marks'][row]
                test_obj.save()

            test_teacher_join = TeacherTestJoin()
            test_teacher_join.test_id = test_id
            test_teacher_join.teacher_id = "lakshya"  # TODO : change from static
            test_teacher_join.save()

            test_information = TestInformation()
            test_information.test_id = test_id
            test_information.type = "Objective"
            test_information.subject = form.cleaned_data.get('subject')
            test_information.topic = form.cleaned_data.get('topic')
            test_information.start_date = form.cleaned_data.get('start_date')
            test_information.start_time = form.cleaned_data.get('start_time')
            test_information.end_date = form.cleaned_data.get('end_date')
            test_information.end_time = form.cleaned_data.get('end_time')
            test_information.duration = form.cleaned_data.get('duration')
            test_information.neg_mark = form.cleaned_data.get('neg_mark')
            test_information.password = form.cleaned_data.get('password')
            test_information.proctor_type = form.cleaned_data.get('proctor_type')
            test_information.save()

            return HttpResponseRedirect('dashboard')
        else:
            return render(request, "teachers/create-test-obj.html", {'form': form.as_p()})

    form = QAUploadForm()
    return render(request, "teachers/create-test-obj.html", {'form': form.as_p()})


def create_test_subjective(request):
    if request.method == 'POST':
        form = QAUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info(form.cleaned_data)

            test_id = generate_slug(2)
            filestream = form.cleaned_data.get('doc')
            filestream.seek(0)
            df = pd.read_csv(filestream)
            fields = ['question_id', 'question', 'marks']
            df = pd.DataFrame(df, columns=fields)

            for row in df.index:
                test_obj = TestSubjective()
                test_obj.test_id = test_id
                test_obj.question_id = df['question_id'][row]
                test_obj.question = df['question'][row]
                test_obj.marks = df['marks'][row]
                test_obj.save()

            test_teacher_join = TeacherTestJoin()
            test_teacher_join.test_id = test_id
            test_teacher_join.teacher_id = "lakshya"  # TODO : change from static
            test_teacher_join.save()

            test_information = TestInformation()
            test_information.type = "Subjective"
            test_information.test_id = test_id
            test_information.subject = form.cleaned_data.get('subject')
            test_information.topic = form.cleaned_data.get('topic')
            test_information.start_date = form.cleaned_data.get('start_date')
            test_information.start_time = form.cleaned_data.get('start_time')
            test_information.end_date = form.cleaned_data.get('end_date')
            test_information.end_time = form.cleaned_data.get('end_time')
            test_information.duration = form.cleaned_data.get('duration')
            test_information.neg_mark = form.cleaned_data.get('neg_mark')
            test_information.password = form.cleaned_data.get('password')
            test_information.proctor_type = form.cleaned_data.get('proctor_type')
            test_information.save()

            return HttpResponseRedirect('dashboard')
        else:
            return render(request, "teachers/create-test-subj.html", {'form': form.as_p()})

    form = QAUploadForm()
    return render(request, "teachers/create-test-subj.html", {'form': form.as_p()})


def view_question(request):
    tests = TestInformation.objects.values_list('test_id', flat=True)
    if request.method == 'POST':
        logging.debug(f"fetching questions for test_id {request.POST}")
        test_id = request.POST['test_id']
        questions = TestObjective.objects.filter(test_id=test_id)
        context = {"tests": tests, "questions": questions}
        return render(request, "teachers/view-questions.html", context=context)

    context = {"tests": tests}
    return render(request, "teachers/view-questions.html", context=context)
