import streamlit as st
from fpdf import FPDF

# School name
school_name = "Al Hamd Cadet Schooling System"

# List of subjects and custom total marks
subjects = ["English", "Urdu", "Math", "Islamiat", "Science", "Social Studies", "Computer", "Arts", "Sindhi", "General Knowledge (GK)"]
subject_max_marks = {
    "English": 100,
    "Urdu": 100,
    "Math": 100,
    "Islamiat": 100,
    "Science": 100,
    "Social Studies": 100,
    "Computer": 75,
    "Arts": 100,
    "Sindhi": 100,
    "General Knowledge (GK)": 50
}

# Function to determine grade based on marks
def get_grade(marks, subject):
    max_marks = subject_max_marks[subject]
    if marks >= 0.9 * max_marks:
        return "A+"
    elif marks >= 0.8 * max_marks:
        return "A"
    elif marks >= 0.7 * max_marks:
        return "B"
    elif marks >= 0.6 * max_marks:
        return "C"
    elif marks >= 0.5 * max_marks:
        return "D"
    else:
        return "F"

# Function to calculate total marks and percentage
def calculate_total_and_percentage(marks):
    total_marks = sum(marks[i] for i in range(len(subjects)))
    total_max_marks = sum(subject_max_marks[subject] for subject in subjects)
    percentage = (total_marks / total_max_marks) * 100
    return total_marks, total_max_marks, percentage

# Function to generate PDF
def generate_pdf(student_name, roll_number, student_class, marks, grades, rank, total_marks, percentage):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt=school_name, ln=True, align='C')
    
    # Student details
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Student Name: {student_name}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Roll Number: {roll_number}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Class: {student_class}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Rank: {rank}", ln=True, align='L')  # Class Rank

    # Subjects, marks, and grades
    pdf.ln(10)
    pdf.cell(100, 10, 'Subject', 1, 0, 'C')
    pdf.cell(50, 10, 'Marks', 1, 0, 'C')
    pdf.cell(40, 10, 'Grade', 1, 1, 'C')

    for i, subject in enumerate(subjects):
        pdf.cell(100, 10, subject, 1, 0, 'C')
        pdf.cell(50, 10, str(marks[i]), 1, 0, 'C')
        pdf.cell(40, 10, grades[i], 1, 1, 'C')

    # Total Marks and Percentage
    pdf.ln(10)
    pdf.cell(100, 10, 'Total Marks', 1, 0, 'C')
    pdf.cell(50, 10, str(total_marks), 1, 1, 'C')
    pdf.cell(100, 10, 'Percentage', 1, 0, 'C')
    pdf.cell(50, 10, f"{percentage}%", 1, 1, 'C')

    # Teacher's and Principal's signature
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(95, 10, 'Teacher\'s Signature: __________________', 0, 0, 'L')
    pdf.cell(95, 10, 'Principal\'s Signature: __________________', 0, 1, 'L')

    # Save PDF
    pdf.output(f"{student_name}_Report_Card.pdf")

# Streamlit UI
def main():
    st.title("Digital Student Report Card System")
    
    # Input student details
    roll_number = st.text_input("Enter Student's Roll Number:")
    student_name = st.text_input("Enter Student's Name:")
    student_class = st.text_input("Enter Student's Class:")
    
    # Input marks for each subject
    marks = []
    grades = []
    all_students_data = []  # To store all students' data for class ranking
    
    for subject in subjects:
        mark = st.number_input(f"Enter marks for {subject} (Max: {subject_max_marks[subject]}):", min_value=0, max_value=subject_max_marks[subject])
        marks.append(mark)
        grades.append(get_grade(mark, subject))

    # Button to generate report card
    if st.button("Generate Report Card"):
        if student_name and roll_number and student_class:
            # Calculate total marks and percentage for the current student
            total_marks, total_max_marks, percentage = calculate_total_and_percentage(marks)
            
            # Simulate class data for ranking (in a real application, this data would come from a database)
            all_students_data.append({
                "student_name": student_name,
                "total_marks": total_marks
            })
            
            # Sort the students based on total marks to determine rank
            all_students_data_sorted = sorted(all_students_data, key=lambda x: x['total_marks'], reverse=True)
            
            # Find the student's rank
            rank = next(i+1 for i, student in enumerate(all_students_data_sorted) if student['student_name'] == student_name)
            
            # Generate the report card PDF
            generate_pdf(student_name, roll_number, student_class, marks, grades, rank, total_marks, percentage)
            
            # Display success message and allow download
            st.success(f"Report Card for {student_name} has been generated with rank {rank}.")
            st.download_button(
                label="Download PDF",
                data=open(f"{student_name}_Report_Card.pdf", "rb").read(),
                file_name=f"{student_name}_Report_Card.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please enter all the student's details (Name, Roll Number, and Class).")

if __name__ == "__main__":
    main()
