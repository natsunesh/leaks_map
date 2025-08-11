import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QLabel, QLineEdit, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.utils import get_user_email
from src.api_client import LeakCheckAPIClient
from src.visualizer_breaches import visualize_breaches_with_info
from src.recommendations import print_recommendations_for_breaches
from datetime import datetime
from typing import List, Dict

class LeakMapGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Leak Map")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.email_label = QLabel("Enter your email:")
        self.layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_input)

        self.check_button = QPushButton("Check for Leaks")
        self.check_button.clicked.connect(self.check_leaks)
        self.layout.addWidget(self.check_button)

        self.export_button = QPushButton("Export Report")
        self.export_button.clicked.connect(self.export_report)
        self.layout.addWidget(self.export_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        self.api_client = LeakCheckAPIClient(api_key=os.getenv("ace07ec3058ee59cabf16c86b0d2e5842060ee41", "ace07ec3058ee59cabf16c86b0d2e5842060ee41"))

        # Add date filter
        self.date_filter_label = QLabel("Filter by date:")
        self.layout.addWidget(self.date_filter_label)

        self.date_filter_input = QLineEdit()
        self.layout.addWidget(self.date_filter_input)

        # Add type filter
        self.type_filter_label = QLabel("Filter by type:")
        self.layout.addWidget(self.type_filter_label)

        self.type_filter_input = QLineEdit()
        self.layout.addWidget(self.type_filter_input)

        # Add sorting option
        self.sort_label = QLabel("Sort by:")
        self.layout.addWidget(self.sort_label)

        self.sort_input = QLineEdit()
        self.layout.addWidget(self.sort_input)

    def check_leaks(self):
        """
        Check for data breaches associated with the entered email address.
        """
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            return

        try:
            breaches = self.api_client.get_breach_info(email)
            if breaches:
                self.result_text.append(f"Found {len(breaches)} breaches for {email}.")
                visualize_breaches_with_info(breaches)
                print_recommendations_for_breaches(breaches, "Russian")
            else:
                self.result_text.append(f"No breaches found for {email}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while checking for breaches: {str(e)}")

    def export_report(self):
        """
        Export the breach report to a text file.
        """
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            return

        try:
            breaches = self.api_client.get_breach_info(email)
            if breaches:
                report_filename = f"{email}_report.txt"
                with open(report_filename, "w") as report_file:
                    for breach in breaches:
                        report_file.write(f"Service: {breach['service_name']}\n")
                        report_file.write(f"Breach Date: {breach['breach_date']}\n")
                        report_file.write(f"Description: {breach['description']}\n")
                        report_file.write("\n")
                QMessageBox.information(self, "Export Successful", f"Report exported successfully to {report_filename}.")
            else:
                QMessageBox.information(self, "No Data", "No breaches found to export.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while exporting the report: {str(e)}")
