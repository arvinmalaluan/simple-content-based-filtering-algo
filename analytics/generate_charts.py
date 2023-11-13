from reportlab.platypus import Image

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as PilImage
from wordcloud import WordCloud


def generate_pie(newget):
    labels = [item['role__role'] for item in newget]
    sizes = [item['count'] for item in newget]

    # Find the index of the max value
    max_index = sizes.index(max(sizes))

    # Create an explode list where all values are 0 except for the max value
    explode = [0.1 if i == max_index else 0 for i in range(len(sizes))]

    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                       shadow=True, startangle=90)

    # Add values to legend
    legend_labels = []
    for label, size in zip(labels, sizes):
        legend_labels.append(f"{label}: {size}")

    # Add a legend
    ax1.legend(wedges, legend_labels, title="Categories",
               loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 12})
    ax1.axis('equal')

    plt.subplots_adjust(left=0, right=1)
    plt.savefig('piechart.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open('piechart.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image('piechart.png', pdf_img_width, pdf_img_height)

    return img


def generate_bar(x1_bc, x2_bc):
    colors = {'With Profile': 'green', 'Without Profile': 'red'}

    categories = ['Without Profile', 'With Profile']
    values = [x2_bc - x1_bc, x1_bc]
    plt.barh(categories, values, color=['red', 'green'])
    plt.xlabel('Counts')
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
               for label in labels]
    plt.legend(handles, labels, loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 12})

    plt.subplots_adjust(left=0, right=1)
    plt.savefig('barchart-ruwnp.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open('barchart-ruwnp.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image('barchart-ruwnp.png', pdf_img_width, pdf_img_height)

    return img


def generate_column(recruiter, seeker):
    categories = ['Batangas', 'Not in Batangas', 'Not set']
    data1 = [item['count'] for item in seeker]
    data2 = [item['count'] for item in recruiter]
    bar_width = 0.35
    bar_positions1 = range(len(categories))
    bar_positions2 = [pos + bar_width for pos in bar_positions1]
    plt.bar(bar_positions1, data1, width=bar_width,
            label='Job Seekers Location Distribution')
    plt.bar(bar_positions2, data2, width=bar_width,
            label='Job Recruiters Location Distribution')
    plt.xticks([pos + bar_width / 2 for pos in bar_positions1], categories)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplots_adjust(left=0, right=1)
    plt.savefig('colchart-ld.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open('colchart-ld.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image('colchart-ld.png', pdf_img_width, pdf_img_height)

    return img


def generate_column_avg_count(value1, value2):
    categories = ['Average Count']
    data1 = [value1]
    data2 = [value2]
    bar_width = 0.35
    bar_positions1 = range(len(categories))
    bar_positions2 = [pos + bar_width for pos in bar_positions1]
    plt.bar(bar_positions1, data1, width=bar_width,
            label='Average Employee Count')
    plt.bar(bar_positions2, data2, width=bar_width,
            label='Average Subsidiary Count')
    plt.xticks([pos + bar_width / 2 for pos in bar_positions1], categories)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplots_adjust(left=0, right=1)
    plt.savefig('colchart-rsr.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open('colchart-rsr.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image('colchart-rsr.png', pdf_img_width, pdf_img_height)

    return img


def generate_column_educational_attainment(value1):
    categories = [item['educational_attainment'] for item in value1]
    data1 = [item['count'] for item in value1]
    bar_width = 0.35
    bar_positions1 = range(len(categories))
    plt.bar(bar_positions1, data1, width=bar_width,
            label='Summary Report on Job Seekers Education Attainment')
    plt.xticks([pos + bar_width / 2 for pos in bar_positions1], categories)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplots_adjust(left=0, right=1)
    plt.savefig('colchart-ea.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open('colchart-ea.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image('colchart-ea.png', pdf_img_width, pdf_img_height)

    return img


def generate_word_cloud(text, title):
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'{title}.jpg', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open(f'{title}.jpg')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image(f'{title}.jpg', pdf_img_width, pdf_img_height)

    return img


def generate_pie_template(labels_temp, values, img_name):
    labels = labels_temp
    sizes = [int(i) for i in values]

    # Find the index of the max value
    max_index = sizes.index(max(sizes))

    # Create an explode list where all values are 0 except for the max value
    explode = [0.1 if i == max_index else 0 for i in range(len(sizes))]

    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                       shadow=True, startangle=90)

    # Add values to legend
    legend_labels = []
    for label, size in zip(labels, sizes):
        legend_labels.append(f"{label}: {size}")

    # Add a legend
    ax1.legend(wedges, legend_labels, title="Categories",
               loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 12})
    ax1.axis('equal')

    plt.subplots_adjust(left=0, right=1)
    plt.savefig(f'{img_name}.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open(f'{img_name}.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image(f'{img_name}.png', pdf_img_width, pdf_img_height)

    return img


def generate_column_template(labels_temp, values, img_name):
    categories = labels_temp
    data1 = values
    bar_width = 0.35
    bar_positions1 = range(len(categories))
    plt.bar(bar_positions1, data1, width=bar_width)
    plt.xticks([pos + bar_width / 2 for pos in bar_positions1], categories)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplots_adjust(left=0, right=1)
    plt.savefig(f'{img_name}.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open(f'{img_name}.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 350
    pdf_img_height = 200
    img = Image(f'{img_name}.png', pdf_img_width, pdf_img_height)

    return img


def generate_barh_template(labels_temp, values_temp, img_name, title):
    labels = labels_temp
    values = values_temp

    # Sort data for better visualization
    sorted_indices = np.argsort(values)
    labels_sorted = [labels[i] for i in sorted_indices]
    values_sorted = [values[i] for i in sorted_indices]

    # Create horizontal bar chart
    plt.figure(figsize=(10, 20))
    plt.barh(labels_sorted, values_sorted, color='skyblue')
    plt.xlabel('Count')
    plt.title(title)

    plt.subplots_adjust(left=0, right=1)
    plt.savefig(f'{img_name}.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    pil_img = PilImage.open(f'{img_name}.png')
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = 450
    pdf_img_height = pdf_img_width / aspect_ratio
    img = Image(f'{img_name}.png', pdf_img_width, pdf_img_height)

    return img
