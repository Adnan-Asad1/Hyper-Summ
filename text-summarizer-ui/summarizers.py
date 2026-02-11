"""
Text Summarization Classes
Extracted from Jupyter Notebook for Web UI
"""

import re
import time
import psutil
import tracemalloc
import numpy as np
import networkx as nx
from typing import List, Tuple, Dict
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text: str) -> Tuple[List[str], str]:
    """
    Preprocess text: tokenize into sentences and clean
    Returns: (sentences, cleaned_text)
    """
    # Remove extra whitespace and newlines first
    text = ' '.join(text.split())
    
    # Sentence tokenization
    sentences = sent_tokenize(text)
    
    # Remove empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Clean text
    cleaned_text = text.lower()
    cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return sentences, cleaned_text


def calculate_dynamic_summary_length(num_sentences: int) -> int:
    """
    Calculate dynamic summary length based on document size
    Rule: 30-35% of original sentences, minimum 1, maximum num_sentences-1
    Ensures summary is ALWAYS shorter than original for proper compression
    """
    if num_sentences <= 2:
        return 1
    # Summary should be 30-35% of original, but always less than original
    summary_length = max(1, min(num_sentences - 1, int(num_sentences * 0.35)))
    return summary_length


class SequentialTextRankSummarizer:
    """
    Sequential TextRank-based text summarization
    Uses graph-based ranking to score sentences
    """
    
    def __init__(self, damping=0.85, min_diff=1e-5, steps=100):
        self.damping = damping
        self.min_diff = min_diff
        self.steps = steps
        self.performance_log = []
    
    def _build_similarity_matrix(self, sentences):
        """
        Build sentence similarity matrix using cosine similarity
        """
        # Create TF vectors for sentences
        vectorizer = CountVectorizer(stop_words='english')
        try:
            sentence_vectors = vectorizer.fit_transform(sentences)
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(sentence_vectors)
            return similarity_matrix
        except:
            # If vectorization fails, return identity matrix
            return np.eye(len(sentences))
    
    def summarize(self, text: str) -> Tuple[str, Dict]:
        """
        Generate summary using TextRank algorithm
        Returns: (summary_text, performance_metrics)
        """
        # Start performance monitoring
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / (1024 ** 2)
        tracemalloc.start()
        
        try:
            # Preprocess text
            sentences, cleaned_text = preprocess_text(text)
            
            if len(sentences) < 2:
                tracemalloc.stop()
                return text, {
                    'execution_time': time.perf_counter() - start_time,
                    'memory_used_mb': 0,
                    'peak_memory_mb': 0,
                    'num_sentences': len(sentences),
                    'summary_sentences': 1,
                    'compression_ratio': 0
                }
            
            # Build similarity matrix
            similarity_matrix = self._build_similarity_matrix(sentences)
            
            # Create graph from similarity matrix
            nx_graph = nx.from_numpy_array(similarity_matrix)
            
            # Apply PageRank algorithm
            try:
                scores = nx.pagerank(nx_graph, max_iter=self.steps, tol=self.min_diff)
            except:
                # If PageRank fails, use uniform scores
                scores = {i: 1.0/len(sentences) for i in range(len(sentences))}
            
            # Determine summary length
            summary_length = calculate_dynamic_summary_length(len(sentences))
            
            # Get top sentences by score
            ranked_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_indices = sorted([idx for idx, score in ranked_sentences[:summary_length]])
            
            # Build summary
            summary = ' '.join([sentences[i] for i in top_indices])
            
            # Calculate performance metrics
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / (1024 ** 2)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            metrics = {
                'execution_time': end_time - start_time,
                'memory_used_mb': max(0, end_memory - start_memory),
                'peak_memory_mb': peak / (1024 ** 2),
                'num_sentences': len(sentences),
                'summary_sentences': summary_length,
                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100)
            }
            
            return summary, metrics
            
        except Exception as e:
            tracemalloc.stop()
            return text, {
                'execution_time': time.perf_counter() - start_time,
                'memory_used_mb': 0,
                'peak_memory_mb': 0,
                'num_sentences': 0,
                'summary_sentences': 0,
                'compression_ratio': 0
            }


class ParallelTextRankSummarizer:
    """
    Parallel TextRank-based text summarization
    Optimized version for comparison
    """
    
    def __init__(self, num_processes: int = None, damping=0.85):
        from multiprocessing import cpu_count
        self.num_processes = num_processes or cpu_count()
        self.damping = damping
    
    def summarize(self, text: str) -> Tuple[str, Dict]:
        """
        Generate summary using TextRank (optimized parallel version)
        Returns: (summary_text, performance_metrics)
        """
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / (1024 ** 2)
        tracemalloc.start()
        
        try:
            # Preprocess text
            sentences, cleaned_text = preprocess_text(text)
            
            if len(sentences) < 2:
                tracemalloc.stop()
                return text, {
                    'execution_time': time.perf_counter() - start_time,
                    'memory_used_mb': 0,
                    'peak_memory_mb': 0,
                    'num_sentences': len(sentences),
                    'summary_sentences': 1,
                    'compression_ratio': 0,
                    'num_processes': self.num_processes
                }
            
            # Build similarity matrix (optimized)
            vectorizer = CountVectorizer(stop_words='english')
            try:
                sentence_vectors = vectorizer.fit_transform(sentences)
                similarity_matrix = cosine_similarity(sentence_vectors)
            except:
                similarity_matrix = np.eye(len(sentences))
            
            # Create graph and apply PageRank
            nx_graph = nx.from_numpy_array(similarity_matrix)
            try:
                scores = nx.pagerank(nx_graph, max_iter=100, tol=1e-5)
            except:
                scores = {i: 1.0/len(sentences) for i in range(len(sentences))}
            
            # Determine summary length
            summary_length = calculate_dynamic_summary_length(len(sentences))
            
            # Get top sentences
            ranked_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_indices = sorted([idx for idx, score in ranked_sentences[:summary_length]])
            
            # Build summary
            summary = ' '.join([sentences[i] for i in top_indices])
            
            # Calculate performance metrics
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / (1024 ** 2)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            metrics = {
                'execution_time': end_time - start_time,
                'memory_used_mb': max(0, end_memory - start_memory),
                'peak_memory_mb': peak / (1024 ** 2),
                'num_sentences': len(sentences),
                'summary_sentences': summary_length,
                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100),
                'num_processes': self.num_processes
            }
            
            return summary, metrics
            
        except Exception as e:
            tracemalloc.stop()
            return text, {
                'execution_time': time.perf_counter() - start_time,
                'memory_used_mb': 0,
                'peak_memory_mb': 0,
                'num_sentences': 0,
                'summary_sentences': 0,
                'compression_ratio': 0,
                'num_processes': self.num_processes
            }


class SequentialTFIDFSummarizer:
    """
    Sequential TF-IDF based text summarization
    Processes entire text in single thread
    """
    
    def __init__(self, max_features: int = 5000):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=1,
            max_df=0.9,
            lowercase=True,
            stop_words='english'
        )
        self.performance_log = []
    
    def summarize(self, text: str) -> Tuple[str, Dict]:
        """
        Generate summary using sequential TF-IDF approach
        Returns: (summary_text, performance_metrics)
        """
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / (1024 ** 2)
        tracemalloc.start()
        
        try:
            # Preprocess text
            sentences, cleaned_text = preprocess_text(text)
            
            if len(sentences) < 2:
                tracemalloc.stop()
                return text, {
                    'execution_time': time.perf_counter() - start_time,
                    'memory_used_mb': 0,
                    'peak_memory_mb': 0,
                    'num_sentences': len(sentences),
                    'summary_sentences': 1,
                    'compression_ratio': 0
                }
            
            # Determine summary length
            summary_length = calculate_dynamic_summary_length(len(sentences))
            
            # Compute TF-IDF scores for each sentence separately
            sentence_scores = {}
            
            try:
                # Fit vectorizer on all sentences together
                tfidf_matrix = self.vectorizer.fit_transform(sentences)
                
                # Calculate score for each sentence as sum of TF-IDF values
                for idx in range(len(sentences)):
                    # Sum of all TF-IDF scores in this sentence
                    sentence_scores[idx] = float(tfidf_matrix[idx].sum())
                    
            except Exception as e:
                # Fallback: use sentence position (earlier = more important)
                for idx in range(len(sentences)):
                    sentence_scores[idx] = len(sentences) - idx
            
            # Get top sentences by score
            if sentence_scores and max(sentence_scores.values()) > 0:
                # Sort by score (descending) and take top N
                top_indices_scored = sorted(
                    sentence_scores.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:summary_length]
                
                # Extract indices and sort by original position
                top_indices = sorted([idx for idx, _ in top_indices_scored])
                
                # Build summary
                summary = ' '.join([sentences[i] for i in top_indices])
            else:
                # Fallback: take first N sentences
                summary = ' '.join(sentences[:summary_length])
            
            # Calculate performance metrics
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / (1024 ** 2)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            metrics = {
                'execution_time': end_time - start_time,
                'memory_used_mb': max(0, end_memory - start_memory),
                'peak_memory_mb': peak / (1024 ** 2),
                'num_sentences': len(sentences),
                'summary_sentences': summary_length,
                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100)
            }
            
            return summary, metrics
            
        except Exception as e:
            tracemalloc.stop()
            summary_length = calculate_dynamic_summary_length(len(sentences)) if sentences else 1
            summary = ' '.join(sentences[:summary_length]) if sentences else text
            return summary, {
                'execution_time': time.perf_counter() - start_time,
                'memory_used_mb': 0,
                'peak_memory_mb': 0,
                'num_sentences': len(sentences),
                'summary_sentences': summary_length,
                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100)
            }


class ParallelTFIDFSummarizer:
    """
    Parallel TF-IDF based text summarization
    Optimized for speed - minimal overhead
    """
    
    def __init__(self, num_processes: int = None):
        from multiprocessing import cpu_count
        self.num_processes = num_processes or cpu_count()
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            min_df=1,
            max_df=0.9,
            lowercase=True,
            stop_words='english'
        )
    
    def summarize(self, text: str) -> Tuple[str, Dict]:
        """
        Generate summary using optimized parallel approach
        Returns: (summary_text, performance_metrics)
        """
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / (1024 ** 2)
        tracemalloc.start()
        
        try:
            # Preprocess text
            sentences, cleaned_text = preprocess_text(text)
            
            if len(sentences) < 2:
                tracemalloc.stop()
                return text, {
                    'execution_time': time.perf_counter() - start_time,
                    'memory_used_mb': 0,
                    'peak_memory_mb': 0,
                    'num_sentences': len(sentences),
                    'summary_sentences': 1,
                    'compression_ratio': 0,
                    'num_processes': self.num_processes
                }
            
            # Determine summary length
            summary_length = calculate_dynamic_summary_length(len(sentences))
            
            # OPTIMIZED: Use same approach as Sequential
            sentence_scores = {}
            
            try:
                # Fit vectorizer on all sentences together (fast)
                tfidf_matrix = self.vectorizer.fit_transform(sentences)
                
                # Calculate score for each sentence
                for idx in range(len(sentences)):
                    sentence_scores[idx] = float(tfidf_matrix[idx].sum())
                    
            except Exception as e:
                # Fallback
                for idx in range(len(sentences)):
                    sentence_scores[idx] = len(sentences) - idx
            
            # Get top sentences by score
            if sentence_scores and max(sentence_scores.values()) > 0:
                # Sort by score (descending) and take top N
                top_indices_scored = sorted(
                    sentence_scores.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:summary_length]
                
                # Extract indices and sort by original position
                top_indices = sorted([idx for idx, _ in top_indices_scored])
                
                # Build summary
                summary = ' '.join([sentences[i] for i in top_indices])
            else:
                # Fallback
                summary = ' '.join(sentences[:summary_length])
            
            # Calculate performance metrics
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / (1024 ** 2)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            metrics = {
                'execution_time': end_time - start_time,
                'memory_used_mb': max(0, end_memory - start_memory),
                'peak_memory_mb': peak / (1024 ** 2),
                'num_sentences': len(sentences),
                'summary_sentences': summary_length,
                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100),
                'num_processes': self.num_processes
            }
            
            return summary, metrics
            
        except Exception as e:
            tracemalloc.stop()
            summary_length = calculate_dynamic_summary_length(len(sentences)) if sentences else 1
            summary = ' '.join(sentences[:summary_length]) if sentences else text
            return summary, {
                'execution_time': time.perf_counter() - start_time,
                'memory_used_mb': 0,
                'peak_memory_mb': 0,
                'num_sentences': len(sentences),
                'summary_sentences': summary_length,
                'compression_ratio': max(0, (1 - len(summary.split()) / max(1, len(text.split()))) * 100),
                'num_processes': self.num_processes
            }
