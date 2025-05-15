import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import markdown

# def generate_report(template_path='template.html', data_path='data.json', output_html='final_report.html', output_pdf='final_report.pdf'):
#     try:
#         env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
#         template = env.get_template(os.path.basename(template_path))

#         with open(data_path, 'r') as f:
#             data = json.load(f)

#         rendered_html = template.render(**data)

#         with open(output_html, 'w') as f:
#             f.write(rendered_html)

#         print(f"HTML report generated: {output_html}")

#         HTML(output_html).write_pdf(output_pdf)
#         print(f"PDF report generated: {output_pdf}")

#     except Exception as e:
#         print(f"Error generating report: {str(e)}")

# if __name__ == "__main__":
#     generate_report()


def generate_report(template_path='template.html', data_path='data.json', output_html='final_report.html', output_pdf='final_report.pdf'):
    try:
        print(f"Loading template from: {template_path}")
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))
        print("Template loaded successfully")

        print(f"Loading data from: {data_path}")
        with open(data_path, 'r') as f:
            data = json.load(f)
        print("Data loaded successfully:", list(data.keys()))

        # Convert Markdown to HTML for each section
        for key in data:
            if data[key]:  # Only convert non-empty strings
                data[key] = markdown.markdown(data[key], extensions=['extra'])
        print("Markdown converted to HTML")

        print("Rendering template...")
        rendered_html = template.render(**data)
        print("Template rendered successfully")

        print(f"Writing HTML to: {output_html}")
        with open(output_html, 'w') as f:
            f.write(rendered_html)
        print(f"HTML report generated: {output_html}")

        print(f"Generating PDF: {output_pdf}")
        HTML(output_html).write_pdf(output_pdf)
        print(f"PDF report generated: {output_pdf}")

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        raise  # Re-raise for debugging

if __name__ == "__main__":
    generate_report()