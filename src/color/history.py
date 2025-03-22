from src.shared.nltk_utils import clean_sentence
from src.shared.utils import similarity, tanh
from colorama import Fore, Style, init
import json, os

init(autoreset = True)

class History:
	def __init__(self, history_path):
		self.history_path = history_path

	def load(self):
		if os.path.isfile(self.history_path) == False:
			with open(self.history_path, "w", encoding="utf-8") as f:
				f.write("[]")

			return []

		with open(self.history_path, "r", encoding="utf-8") as f:
			return json.load(f)

	def delete(self):
		print(f"{Fore.YELLOW}{Style.BRIGHT}Deleting History")

		with open(self.history_path, "w", encoding="utf-8") as f:
			f.write("[]")

		return []

	def update(self, text, results, total_results):
		history = self.load()

		# just return the loaded history if same query exist in history
		if text.lower() in [i["query"].lower() for i in history]:
			return history

		# update history
		history.append(
			{
				"query": text,
				"results": results,
				"total_results": total_results
			}
		)

		with open(self.history_path, "w", encoding="utf-8") as f:
			json.dump(history, f, indent=4)

		return history

	def search(self, query):
		history = self.load()

		if not history:
			return [{
				"query": query,
				"results": [{"Title": "", "URL": ""}],
				"total_results": 0
			}, 0]

		raw_query = query.lower()
		cleaned_query = clean_sentence(raw_query)
		query_tokens = set(cleaned_query.split())
		ranked_results = []

		for h in history:
			raw_title = h["query"].lower().strip()
			cleaned_title = clean_sentence(raw_title)
			title_tokens = set(cleaned_title.split())

			# fast token overlap calculation
			matches = query_tokens.intersection(title_tokens)
			match_count = len(matches)

			# calculate percentage of query tokens found in title
			query_coverage = match_count / len(query_tokens) if query_tokens else 0

			# consider the length ratio between raw and cleaned text
			# this rewards titles with higher information density (less stop words)
			query_density = len(cleaned_query) / len(raw_query) if raw_query else 0
			title_density = len(cleaned_title) / len(raw_title) if raw_title else 0
			density_similarity = similarity(query_density, title_density)

			# find the relative positions of matching terms
			# (rewards titles where matching terms appear earlier)
			position_score = 0
			if match_count > 0:
				for i, token in enumerate(title_tokens):
					# earlier positions get higher scores
					if token in query_tokens:
						position_score += 1 / (i + 1)

			# combined score with weights
			score = (query_coverage * 5.0 + density_similarity * 2.0 + position_score * 1.5 + match_count)/4

			# optional: boost exact title matches
			if cleaned_query == cleaned_title:
				score *= 2

			# apply tanh scaling to squeeze score b\w -1 and 1
			ranked_results.append((h, (1 + tanh(score)) * 0.5))
		ranked_results.sort(key=lambda x: x[1], reverse=True)
		return ranked_results[0]
