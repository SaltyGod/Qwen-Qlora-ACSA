import os
import json
from sklearn.metrics import precision_recall_fscore_support

def evaluate_performance(file_path):
    # Initialize dimension names and accuracy counters
    dimensions = [
        "Location#Transportation", "Location#Downtown", "Location#Easy_to_find",
        "Service#Queue", "Service#Hospitality", "Service#Parking", "Service#Timely",
        "Price#Level", "Price#Cost_effective", "Price#Discount",
        "Ambience#Decoration", "Ambience#Noise", "Ambience#Space", "Ambience#Sanitary",
        "Food#Portion", "Food#Taste", "Food#Appearance", "Food#Recommendation"
    ]

    # Read and parse jsonl file
    y_true = []  # True labels
    y_pred = []  # Predicted labels
    for line in open(file_path, 'r', encoding='utf-8'):
        # Parse each line of json data
        data = json.loads(line)
        output = data["conversation"][0]["output"]
        pred_output = data["conversation"][0]["PredOutput"]

        # Split and convert label strings to dictionaries
        output_dict = dict(item.split(': ') for item in output.strip().split(', '))
        pred_output_dict = dict(item.split(': ') for item in pred_output.strip().split(', '))

        # Update true and predicted labels
        y_true.append([output_dict.get(dim, 'None') for dim in dimensions])
        y_pred.append([pred_output_dict.get(dim, 'None') for dim in dimensions])

    # Calculate precision, recall, and F1 score for each dimension
    precision_dim = {}
    recall_dim = {}
    f1_score_dim = {}
    accuracy_dim = {}
    for dim, idx in zip(dimensions, range(len(dimensions))):
        precision_dim[dim], recall_dim[dim], f1_score_dim[dim], _ = precision_recall_fscore_support(
            [label[idx] for label in y_true], [label[idx] for label in y_pred], average='macro'
        )
        accuracy_dim[dim] = sum([1 for true_label, pred_label in zip([label[idx] for label in y_true], [label[idx] for label in y_pred]) if true_label == pred_label]) / len(y_true) * 100

    # Calculate precision, recall, and F1 score for overall
    precision_total, recall_total, f1_score_total, _ = precision_recall_fscore_support(
        [label for sublist in y_true for label in sublist],
        [label for sublist in y_pred for label in sublist],
        average='macro'
    )
    accuracy_total = sum([1 for true_label, pred_label in zip([label for sublist in y_true for label in sublist], [label for sublist in y_pred for label in sublist]) if true_label == pred_label]) / len([label for sublist in y_true for label in sublist]) * 100

    # Build result dictionary
    performance_results = {}
    for dim in dimensions:
        performance_results[dim] = {
            "Accuracy": accuracy_dim[dim],
            "Recall": recall_dim[dim],
            "F1 Score": f1_score_dim[dim]
        }
    performance_results["Overall"] = {
        "Accuracy": accuracy_total,
        "Recall": recall_total,
        "F1 Score": f1_score_total
    }

    return performance_results

def save_results_to_txt(results, output_file):
    # Create directory if it doesn't exist
    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(output_file, 'w') as f:
        f.write("Sentiment Prediction Metrics:\n")
        for dim, values in results.items():
            f.write(f"{dim}:\n")
            for metric, value in values.items():
                f.write(f"\t{metric}: {value}\n")
            f.write("\n")
