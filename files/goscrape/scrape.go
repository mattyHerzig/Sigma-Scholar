package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"net/url"

	"github.com/PuerkitoBio/goquery"
)
func urljoin(base, href string) string {
	baseURL, err := url.Parse(base)
	if err != nil {
		return ""
	}

	absoluteURL, err := baseURL.Parse(href)
	if err != nil {
		return ""
	}

	return absoluteURL.String()
}

func getLinksFromWebpage(url string) ([]string, error) {
	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("Failed to fetch the webpage. Status code: %d", response.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		return nil, err
	}

	var links []string
	doc.Find("#dir-list a").Each(func(_ int, s *goquery.Selection) {
		href, _ := s.Attr("href")
		links = append(links, urljoin(url, href))
	})

	return links, nil
}

func getLinksByClass(url, className string) ([]string, error) {
	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("Failed to fetch the webpage. Status code: %d", response.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		return nil, err
	}

	var links []string
	doc.Find(fmt.Sprintf("a.%s", className)).Each(func(_ int, s *goquery.Selection) {
		href, _ := s.Attr("href")
		links = append(links, urljoin(url, href))
	})

	return links, nil
}

func getLinksFromTable(url string) ([]string, error) {
	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("Failed to fetch the webpage. Status code: %d", response.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		return nil, err
	}

	var links []string
	doc.Find("table a").Each(func(_ int, s *goquery.Selection) {
		href, _ := s.Attr("href")
		links = append(links, urljoin(url, href))
	})

	return links, nil
}

func getTextFromElements(url string, elementIDs []string) (map[string]string, error) {
	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("Failed to fetch the webpage. Status code: %d", response.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		return nil, err
	}

	elementTexts := make(map[string]string)
	for _, elementID := range elementIDs {
		elementTexts[elementID] = doc.Find(fmt.Sprintf("#%s", elementID)).Text()
	}

	return elementTexts, nil
}

// Replace hyphens with space if it exists
func replaceHyphensWithSpace(inputString string) string {
	parts := strings.Split(inputString, "-")
	for i := range parts {
		parts[i] = strings.ReplaceAll(parts[i], "-", " ")
	}
	return strings.Join(parts, " ")
}

func getSubdirectories(url string) []string {
	parsedURL, _ := url.Parse(url)
	pathComponents := strings.Split(parsedURL.Path, "/")
	var subdirectories []string
	for _, component := range pathComponents {
		if component != "" {
			subdirectories = append(subdirectories, replaceHyphensWithSpace(component))
		}
	}
	return subdirectories
}

func extractPage(link string) (string, error) {
	extractDict := []string{"page-name", "header-items-award-detail-inner-wrapper", "description"}

	elementTexts, err := getTextFromElements(link, extractDict)
	if err != nil {
		return "", err
	}

	firstKey := ""
	firstValue := ""
	for key, value := range elementTexts {
		firstKey = key
		firstValue = value
		break
	}

	subs := getSubdirectories(link)
	output := fmt.Sprintf("Scholarship: %s\ncategories: [%s, %s]\n website url:%s\n Extracted from website:\n",
		firstValue, subs[len(subs)-3], subs[len(subs)-2], link)

	for elementID, text := range elementTexts {
		output += fmt.Sprintf("%s: %s\n", elementID, text)
	}

	return output, nil
}

func writeToFile(output []string, filename string) error {
	content := strings.Join(output, "\n")
	return ioutil.WriteFile(filename, []byte(content), 0644)
}

func main() {
	allLinks, err := getLinksFromWebpage("https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	allDocs := make([]string, 0)

	for _, src := range allLinks {
		output, err := extractPage(src)
		if err != nil {
			fmt.Println("Error:", err)
			return
		}
		allDocs = append(allDocs, output)
	}

	err = writeToFile(allDocs, "output.txt")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Output has been written to 'output.txt'")
}
