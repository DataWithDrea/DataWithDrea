"""
MatchMaker.AI main script
This script provides a command-line interface for analyzing resume and job posting keywords.
"""

import argparse
import re
from collections import Counter

def tokenize(text):
    # simple tokenizer: lowercase, remove non-alphabetic, split
    tokens = re.findall(r'[A-Za-z]+', text.lower())
    return tokens

def extract_keywords(text, stopwords=None):
    tokens = tokenize(text)
    if stopwords:
        tokens = [t for t in tokens if t not in stopwords]
    counts = Counter(tokens)
    return counts

def compute_match_score(resume_counts, job_counts):
    # intersection of words: sum of min counts of each word in both
    match_words = set(resume_counts) & set(job_counts)
    matched = sum(min(resume_counts[w], job_counts[w]) for w in match_words)
    total_job = sum(job_counts.values())
    score = matched / total_job if total_job else 0
    return score, match_words

def main():
    parser = argparse.ArgumentParser(description="MatchMaker.AI: simple keyword-based resume matcher.")
    parser.add_argument("resume_file", help="Path to the resume text file")
    parser.add_argument("job_file", help="Path to the job description text file")
    args = parser.parse_args()

    with open(args.resume_file, "r", encoding="utf-8") as f:
        resume_text = f.read()
    with open(args.job_file, "r", encoding="utf-8") as f:
        job_text = f.read()

    # basic english stopwords list
    stopwords = set([
        "and","the","to","of","in","a","for","with","on","at","by","an","be","is","are","from","or","as","that","this","it","your"
    ])

    resume_counts = extract_keywords(resume_text, stopwords)
    job_counts = extract_keywords(job_text, stopwords)

    score, match_words = compute_match_score(resume_counts, job_counts)
    print(f"Match score: {score*100:.2f}%")
    if match_words:
        print("Matched keywords:", ", ".join(sorted(match_words)))
    else:
        print("No keyword matches found. Consider tailoring your resume to the job description.")

if __name__ == "__main__":
    main()
