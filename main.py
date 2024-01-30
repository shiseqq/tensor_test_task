from selenium import webdriver
import Tests


Tests.test_first_bench(webdriver.Chrome())
Tests.test_second_bench(webdriver.Chrome())
Tests.test_third_bench(webdriver.Chrome())
