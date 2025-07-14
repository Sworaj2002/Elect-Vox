
import pymysql
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import RegistrationForm, LoginForm, CandidateRegistrationForm
#from django.contrib.auth.decorators import login_required


# DB Connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Sworaj@1235',
        database='voter',
        cursorclass=pymysql.cursors.DictCursor
    )

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']  
            dob = form.cleaned_data['date_of_birth']

            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            aadhar = form.cleaned_data['aadhar']

            connection = get_db_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users (name, email, phone_number, password, date_of_birth, age, aadhar)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (name, email, phone, password, dob, age, aadhar))
                connection.commit()

            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']

            connection = get_db_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s OR phone_number = %s",
                                   (email_or_phone, email_or_phone))
                    user = cursor.fetchone()

            if user and password == user['password']:
                request.session['user_id'] = user['id']
                request.session['user_name'] = user['name']
                request.session['is_staff'] = user.get('is_staff', False)

                if user.get('is_staff', False):
                    return redirect('admin_dashboard')
                else:
                    return redirect('voter_dashboard')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def voter_dashboard(request):
    return render(request, 'voter.html', {'user': request.session.get('user_name')})

def admin_dashboard(request):
    return render(request, 'admin.html', {'user': request.session.get('user_name')})

def demo(request):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    return render(request, 'demo.html', {'users': users})



def create_elections(request):
    return render(request, 'admin/create_elections.html')

def manage_elections(request):
    return render(request, 'admin/manage_elections.html')

def approve_candidates(request):
    connection = get_db_connection()

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        action = request.POST.get('action')  

        if candidate_id and action in ['approve', 'reject']:
            status = 'approved' if action == 'approve' else 'rejected'
            try:
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE register_candidate SET status = %s WHERE id = %s",
                            (status, candidate_id)
                        )
                    connection.commit()
                messages.success(request, f"Candidate {status.capitalize()} successfully.")
            except Exception as e:
                messages.error(request, "Error updating candidate status.")
        else:
            messages.error(request, "Invalid request.")

        return redirect('approve_candidates') 

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM register_candidate")
            candidates = cursor.fetchall()

    return render(request, 'admin/approve_candidates.html', {'candidates': candidates})


def view_results(request):
    return render(request, 'admin/view_results.html')


def voter_logs(request):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    return render(request, 'admin/voter_logs.html', {'users': users})


def view_election(request):
    return render(request, 'voter/view_election.html')


def register_candidate(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            aadhar_number = form.cleaned_data['aadhar_number']
            voter_id = form.cleaned_data['voter_id']
            manifesto = form.cleaned_data['manifesto']
            supporters_names = form.cleaned_data['supporters_names']

            photo_file = form.cleaned_data['photo']
            photo_binary = photo_file.read() if isinstance(photo_file, InMemoryUploadedFile) else None

            connection = get_db_connection()
            try:
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO register_candidate 
                            (full_name, photo, aadhar_number, voter_id, manifesto, supporters_names, status) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                            full_name, photo_binary, aadhar_number,
                            voter_id, manifesto, supporters_names, 'pending'
                        ))
                    connection.commit()
                    messages.success(request, "Candidate registration submitted!")
                    return redirect('voter_dashboard')
            except Exception as e:
                connection.rollback()
                print("DB Error:", e)
                messages.error(request, "Something went wrong. Please try again.")
    else:
        form = CandidateRegistrationForm()

    return render(request, 'voter/register-candidate.html', {'form': form})



def candidate_status(request):
    status_message = None
    note_message = None
    voter_id = ''

    if request.method == "POST":
        voter_id = request.POST.get('voter_id', '').strip()

        if voter_id:
            connection = get_db_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT status FROM register_candidate WHERE voter_id = %s",
                        (voter_id,)
                    )
                    candidate = cursor.fetchone()

            if candidate:
                status = candidate['status'].lower()
                if status == 'pending':
                    status_message = "Pending"
                    note_message = "Your registration is under review. Please wait for approval."
                elif status == 'approved':
                    status_message = "Approved"
                    note_message = "You are approved. You are eligible to campaign."
                elif status == 'rejected':
                    status_message = "Rejected"
                    note_message = "Your registration has been rejected."
                else:
                    status_message = status.capitalize()
                    note_message = "Status unknown. Please contact support."
            else:
                status_message = "Not Found"
                note_message = "No candidate found with this Voter ID."
        else:
            status_message = "Error"
            note_message = "Please enter a Voter ID."

    return render(request, 'voter/candidate-status.html', {
        'status_message': status_message,
        'note_message': note_message,
        'voter_id': voter_id
    })


def results(request):
    return render(request, 'voter/results.html')


def election_history(request):
    return render(request, 'voter/election-history.html')


def rules(request):
    return render(request, 'voter/rules.html')
