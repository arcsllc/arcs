
{
    'name': 'ARCS - Payroll',
    'category': 'Human Resources/Payroll',
    'depends': ['hr_payroll'],
    'description': """
ARCS - Payroll Rules.
======================

    * Employee Contracts
    * Allowances/Deductions
    * Allow to configure Basic/Gross/Net Salary
    * Employee Payslip
    * Monthly Payroll Register
    * Integrated with Leaves Management
    * Withholding Tax
    """,

    'data': [
 
        'views/hr_contract_form.xml',
       
    ],
    
    'auto_install': False,
    'license': 'AGPL-3',
}
