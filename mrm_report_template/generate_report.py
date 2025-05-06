import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def generate_report(template_path='template.html', data_path='reportData.json', output_html='final_report.html', output_pdf='final_report.pdf'):
    try:
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))

        with open(data_path, 'r') as f:
            data = json.load(f)

        rendered_html = template.render(**data)

        with open(output_html, 'w') as f:
            f.write(rendered_html)

        print(f"HTML report generated: {output_html}")

        HTML(output_html).write_pdf(output_pdf)
        print(f"PDF report generated: {output_pdf}")

    except Exception as e:
        print(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    generate_report()