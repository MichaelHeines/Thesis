// Function that finds the 2 maximum values for a histogram, within given ranges, then calibrates on two peaks and returns [intercept, slope]
array<Double_t, 2> calibration(TH1F* histo, Double_t calibs[2], Int_t ranges[4]) {
	array<Double_t, 2> peaks;

	histo->GetXaxis()->SetRangeUser(ranges[0], ranges[1]);
	int binmax = histo->GetMaximumBin();
	peaks[0] = histo->GetXaxis()->GetBinCenter(binmax);

	histo->GetXaxis()->SetRangeUser(ranges[2], ranges[3]);
	binmax = histo->GetMaximumBin();
	peaks[1] = histo->GetXaxis()->GetBinCenter(binmax);

	array<Double_t, 2> CtoE;
	CtoE[1] = (peaks[1] - peaks[0]) /(calibs[1] - calibs[0]);
	CtoE[0] = -CtoE[1]*calibs[0] + peaks[0];
		
	return CtoE;
}

// Function that gets the channel number for a given energy
Double_t get_channel(array<Double_t, 2> calibs, Double_t energy) {
	Double_t channel;
	channel = calibs[0] + energy * calibs[1];
	return channel;
}

// Function that estimates the background on a spectrum
void populate_background(TH1F* histogram, TH1F* bg_histogram, Int_t xmax) {
	//histogram->Draw("L");
	TSpectrum* s = new TSpectrum();
	Double_t* source = new Double_t[xmax];
	for (int i = 0; i < xmax; i++) source[i] = histogram->GetBinContent(i + 1);
	s->Background(source, xmax, 4, 1, 0, kFALSE, 3, kTRUE);
	for (int i = 0; i < xmax; i++) bg_histogram->SetBinContent(i + 1, source[i]);
	bg_histogram->SetLineColor(kRed);
	//bg_histogram->Draw("SAME L");
	//gPad->SetLogy();
	//histogram->SetXTitle("Energy (channels)");
	//histogram->SetYTitle("Counts");
}

// Function that fits histogram in a range to a quadratic+gaussian and returns gaussian integral counts + error + peakmean
array<Double_t, 3> get_counts(Double_t energy, TH1F* histo, Int_t range, array<Double_t, 2> cal) {
	Int_t channel = TMath::Nint(cal[0] + cal[1] * energy);
	histo->GetXaxis()->SetRangeUser(channel - range, channel + range);
	Int_t binmax = histo->GetMaximumBin();
	Double_t peak = histo->GetXaxis()->GetBinCenter(binmax);
	Double_t maximum = histo->GetMaximum();


	//TF1* fit = new TF1("fit", "[0]* exp(-(x-[1])*(x-[1])/2./[2]/[2]) + [3] + [4]*x", channel - range, channel + range);
	//fit->SetParNames("Amplitude", "Mean", "Sigma", "intercept", "slope");
	//fit->SetParameters(maximum, peak, 2, 0, 0);
	
	TF1* fit = new TF1("fit", "gaus", channel - range, channel + range);
	
	//TF1* fit = new TF1("fit", "gaus", channel - range, channel + range);
	//fit->SetParNames("Amplitude", "Mean", "Sigma");
	//fit->SetParameters(maximum, peak, 2);

	histo->Fit("fit", "q");
	
	Double_t p0 = fit->GetParameter(0);		// Amplitude
	Double_t p1 = fit->GetParameter(1);		// Mean
	Double_t p2 = fit->GetParameter(2);		// Std
	Double_t e0 = fit->GetParError(0);
	Double_t e1 = fit->GetParError(1);
	Double_t e2 = fit->GetParError(2);
	array<Double_t, 3> result;

	result[0] = p0 * abs(p2) * sqrt(2.0 * TMath::Pi());								// Gaussian integral
	result[1] = result[0] * sqrt((e0 / p0)* (e0 / p0) + (e2 / p2)* (e2 / p2));		// Error on integral
	result[2] = p1;																	// Mean
	return result;
}

//Adds files in a folder to a chain
void add_files_to_chain(TChain* chain, TString startstring, TString endstring, TString directory) {
	const char* dirname = directory;//"/mnt/ksf9/H2/user/r0795801/_IO/MEDICIS/MED024_2020/Nov/Coincidence/raw_data/" + directory;
	//const char* dirname = homedir + directory;
	cout << dirname << endl;
	const char* ext = ".root";
	vector<TString> filenames;
	int added = 0;
	TSystemDirectory dir(dirname, dirname);
	TList* files = dir.GetListOfFiles();

	if (files) {
		TSystemFile* file;
		TString fname;
		TIter next(files);

		while ((file = (TSystemFile*)next())) {
			fname = file->GetName();

			if (!file->IsDirectory() && fname.EndsWith(endstring) && fname.BeginsWith(startstring)) {

				//get  list of file names.
				filenames.push_back(fname);
				++added;
			}
		}

		sort(filenames.begin(), filenames.end());
		for (int i = 0; i < added - 1;) {
			if (filenames[i + 1].Sizeof() < filenames[i].Sizeof()) {
				TString temp = filenames[i];
				filenames[i] = filenames[i + 1];
				filenames[i + 1] = temp;
				i = 0;
			}
			i++;
		}

		Int_t i = 0;
		for (std::vector<TString>::iterator it = filenames.begin(); it != filenames.end(); ++it) {
	
			if (i < 50) {
				std::cout << *it << "\n";
				chain->Add(dirname + *it);
			}
			i++;
		}
	}

	cout << added << " files have been added " << "\n";
}

//calculates integral of bins
ULong64_t bin_integral(Double_t energy, TH1F* histogram, Int_t hwidth, array<Double_t, 2> cal) {
	Int_t peak = round(energy);
	histogram->GetXaxis()->SetRangeUser(peak - hwidth, peak + hwidth);
	Int_t lower = peak - hwidth;
	Int_t upper = peak + hwidth;
	ULong64_t integral;

	integral = histogram->Integral(histogram->FindBin(lower), histogram->FindBin(upper));
	histogram->Draw();

	return integral;
}


int Get_activities() {
	//TFile* f = new TFile("m108/MED024_M108_0/RAW/DataR_MED024_M108_6.root");		// Load the root file
	//TTree* mytree; f->GetObject("Data_R", mytree);							// make a pointer to the tree
	
	//const Int_t nr_dirs = 7;
	//TString ls_dirs[nr_dirs] = { "m108/MED024_M108_0/RAW/", "m108/MED024_M108_2/RAW/", "m108/MED024_M108_3/RAW/", "m108/MED024_M108_4/RAW/", "m108/MED024_M108_5/RAW/", "m108/MED024_M108_6/RAW/", "m108/MED024_M108_7/RAW/"};
	//ofstream myFile("M108_data points_binI_scaledroot.csv");//, std::ios_base::app);
	//Double_t rel_counts_approx[nr_dirs] = { 1, 0.75116204, 0.69188878, 0.57360239, 0.43160069, 0.27957707, 0.15220823 };// ,0.00858223
	const Int_t nr_dirs = 6;
	TString ls_dirs[nr_dirs] = { "m120/MED024_M120_1/RAW/", "m120/MED024_M120_2/RAW/", "m120/MED024_M120_3/RAW/", "m120/MED024_M120_4/RAW/", "m120/MED024_M120_5/RAW/", "m120/MED024_M120_6/RAW/" };
	ofstream myFile("M120_data points_binI_scaledroot.csv");//, std::ios_base::app);
	Double_t rel_counts_approx[nr_dirs] = { 1., 0.86730604, 0.58192843, 0.35190774, 0.20095604, 0.13213929 };
	myFile << "Folder " << ";" << "Time since start" << ";" << "Measurement time" << ";" << "Bi A" << ";" << "Bi A relerr" << ";" << "Tl A" << ";" << "Tl A relerr" << endl;
	//TString mydir = gSystem->pwd();

	for (Int_t l = 0; l < nr_dirs; l++) {
		TString this_dir = ls_dirs[l];
		cout << this_dir << endl;

		TChain* mytree = new TChain("Data_R");
		add_files_to_chain(mytree, "DataR", ".root", this_dir);
		cout << "Added files" << endl;

	
		TBranch* Energy_branch = mytree->GetBranch("Energy");						// Assign the branches
		TBranch* Channel_branch = mytree->GetBranch("Channel");
		TBranch* Time_branch = mytree->GetBranch("Timestamp");
		UShort_t energy;															// Define the datatypes of the leaves
		UShort_t channel;
		ULong64_t time;
		mytree->SetBranchAddress("Energy", &energy);								// Sets the branches to a variable
		mytree->SetBranchAddress("Channel", &channel);
		mytree->SetBranchAddress("Timestamp", &time);

		const Int_t entry = mytree->GetEntries();									// Number of entries in the root file
		cout << entry << endl;


		Int_t num_points;
		Double_t temp = (entry / 50e06) * (1 / sqrt(rel_counts_approx[l]));
		if (temp <= 1) {
			num_points = 1;
		}
		else {
			num_points = ceil(temp);
		}
		//Int_t entry_perpoint = round((entry / 50e06) * (1 / rel_counts_approx[l]));


		for (Int_t k = 0; k < num_points; k++) {
			Int_t entry_perpoint = round(entry /(num_points));
			TH1F* h0 = new TH1F("h0", "Energy spectrum", 2000, 0, 2000);				// Initialize histogram and canvas
			TH1F* h1 = new TH1F("h1", "Energy spectrum", 2000, 0, 2000);
			TH1F* bg0 = new TH1F("bg0", "The background of histo channel 0", 2000, 0, 2000);
			TH1F* bg1 = new TH1F("bg1", "The background of histo channel 1", 2000, 0, 2000);
			TCanvas* c1 = new TCanvas("c1", "Spectrum", 200, 10, 600, 400);

			for (Int_t i = 0; i < entry_perpoint; i++) {								// Iterate over leaves
				mytree->GetEntry(i + k * entry_perpoint);								// Get a leaf in all of the branches

				if (channel == 0) {														// Fill the energy leave into the correct histogram
					h0->Fill(energy);
				}
				else if (channel == 1) {
					h1->Fill(energy);
				}
			}
			cout << "Got histogram" << endl;

			TH1F* h0_peaks = (TH1F*)h0->Clone("h0");									// Obtain background subtracted histograms
			TH1F* h1_peaks = (TH1F*)h1->Clone("h1");
			populate_background(h0, bg0, 2000);
			populate_background(h1, bg1, 2000);
			h0_peaks->Add(bg0, -1);
			h1_peaks->Add(bg1, -1);

			cout << "Subtracted background" << endl;

			Double_t calibrations[2] = { 218.0, 440.45 };								// Make quick calibrations for both detectors, accurate to about 2 Channels
			Int_t range[4] = { 150, 250, 400, 450 };
			array<Double_t, 2> cal0; cal0 = calibration(h0, calibrations, range);
			array<Double_t, 2> cal1; cal1 = calibration(h1, calibrations, range);


			const Int_t n = 4;
			Double_t desired_peaks[n] = { 807.36, 292.8, 465.14, 1567.08 };				// Peaks we want to fit for coincidences
			Double_t channels0[n];
			Double_t channels1[n];

			for (Int_t i = 0; i < n; i++) {												// Get channels for desired peaks
				channels0[i] = get_channel(cal0, desired_peaks[i]);
			}
			for (Int_t i = 0; i < n; i++) {
				channels1[i] = get_channel(cal1, desired_peaks[i]);
			}

			h0_peaks->GetXaxis()->SetRangeUser(0, 2000);								// Reset the ranges
			h1_peaks->GetXaxis()->SetRangeUser(0, 2000);

			const Double_t hwidth = 10;
			ULong64_t counts0[n];
			Double_t errors0[n];
			ULong64_t counts1[n];
			Double_t errors1[n];
			Double_t peaks0[n];
			Double_t peaks1[n];


			for (Int_t i = 0; i < n; i++) {												// Obtains counts and errors and mean of the peaks
				
				ULong64_t bin_I0 = bin_integral(channels0[i], h0_peaks, hwidth, cal0);
				counts0[i] = bin_I0;
				errors0[i] = 0;
				peaks0[i] = channels0[i];
				/*
				h0_peaks->GetXaxis()->SetRangeUser(channels0[i] - hwidth, channels0[i] + hwidth);
				array<Double_t, 3> fitting = get_counts(desired_peaks[i], h0_peaks, hwidth, cal0);
				counts0[i] = fitting[0];
				errors0[i] = fitting[1];
				peaks0[i] = fitting[2];
				*/
			}

			for (Int_t i = 0; i < n; i++) {
				
				ULong64_t bin_I1 = bin_integral(channels1[i], h1_peaks, hwidth, cal1);
				counts1[i] = bin_I1;
				errors1[i] = 0;
				peaks1[i] = channels1[i];
				/*
				h1_peaks->GetXaxis()->SetRangeUser(channels1[i] - hwidth, channels1[i] + hwidth);
				array<Double_t, 3> fitting = get_counts(desired_peaks[i], h1_peaks, hwidth, cal1);
				counts1[i] = fitting[0];
				errors1[i] = fitting[1];
				peaks1[i] = fitting[2];
				*/
			}


			Double_t N1_Bi_0 = counts0[0];													// Assigns appropriate counts _detector
			Double_t N2_Bi_0 = counts0[1];
			Double_t N1_Tl_0 = counts0[2];
			Double_t N2_Tl_0 = counts0[3];
			Double_t N1_Bi_1 = counts1[0];
			Double_t N2_Bi_1 = counts1[1];
			Double_t N1_Tl_1 = counts1[2];
			Double_t N2_Tl_1 = counts1[3];
			Double_t e1_Bi_0 = errors0[0];													// Assigns appropriate errors _detector
			Double_t e2_Bi_0 = errors0[1];
			Double_t e1_Tl_0 = errors0[2];
			Double_t e2_Tl_0 = errors0[3];
			Double_t e1_Bi_1 = errors1[0];
			Double_t e2_Bi_1 = errors1[1];
			Double_t e1_Tl_1 = errors1[2];
			Double_t e2_Tl_1 = errors1[3];
			Double_t mean1_Bi_0 = peaks0[0];												// Assigns appropriate peak locations _detector
			Double_t mean2_Bi_0 = peaks0[1];
			Double_t mean1_Tl_0 = peaks0[2];
			Double_t mean2_Tl_0 = peaks0[3];
			Double_t mean1_Bi_1 = peaks1[0];
			Double_t mean2_Bi_1 = peaks1[1];
			Double_t mean1_Tl_1 = peaks1[2];
			Double_t mean2_Tl_1 = peaks1[3];

			ULong64_t t0;
			ULong64_t t1;
			ULong64_t dt;
			UShort_t e0;
			UShort_t e1;
			ULong64_t window = 200000;
			Double_t coinc_Bi_01 = 0;
			Double_t coinc_Bi_10 = 0;
			Double_t coinc_Tl_01 = 0;
			Double_t coinc_Tl_10 = 0;
			Double_t counts = 0;


			TH1F* hcoinc = new TH1F("hcoinc", "Energy spectrum", 2000, 0, 2000);			// Can be used to check present coincidence energies

			for (Int_t i = 10; i < entry_perpoint - 10; i++) {								// Iterate over all events
				mytree->GetEntry(i + k * entry_perpoint);

				if (channel == 0) {															// If the event is in detector 0
					t0 = time;
					e0 = energy;

					if (abs(e0 - mean1_Bi_0) <= 10) {										// Energy is in 807 keV interval --> Look for 293 keV second photon
						for (Int_t j = -10; j < 10; j++) {									// Check -10 to +10 events
							mytree->GetEntry(i + k * entry_perpoint + j);
							t1 = time;

							if (t1 > t0) {
								dt = t1 - t0;
							}
							else {
								dt = t0 - t1;
							}

							if ((channel == 1) and (dt <= window)) {							// If the second photon is in coincidence and in detector 1
								e1 = energy;
								if (abs(e1 - mean2_Bi_1) <= 10) {							// If the second photon is in the 293 keV interval
									coinc_Bi_01 += 1;										// 01 order Bi event
								}
							}
						}
					}
					else if (abs(e0 - mean2_Bi_0) <= 10) {									// Energy is in 293 keV interval --> Look for 807 keV second photon
						for (Int_t j = -10; j < 10; j++) {									// Check -10 to +10 events
							mytree->GetEntry(i + j + k * entry_perpoint);
							t1 = time;

							if (t1 > t0) {
								dt = t1 - t0;
							}
							else {
								dt = t0 - t1;
							}

							if ((channel == 1) and (dt <= window)) {						// If the second photon is in coincidence and in detector 1
								e1 = energy;
								if (abs(e1 - mean1_Bi_1) <= 10) {							// If the second photon is in the 293 keV interval
									coinc_Bi_10 += 1;										// 10 order Bi event
								}
							}
						}
					}
					else if (abs(e0 - mean1_Tl_0) <= 10) {									// Energy is in 293 keV interval --> Look for 807 keV second photon
						for (Int_t j = -10; j < 10; j++) {									// Check -10 to +10 events
							mytree->GetEntry(i + j + k * entry_perpoint);
							t1 = time;

							if (t1 > t0) {
								dt = t1 - t0;
							}
							else {
								dt = t0 - t1;
							}

							if ((channel == 1) and (dt <= window)) {						// If the second photon is in coincidence and in detector 1
								e1 = energy;
								if (abs(e1 - mean2_Tl_1) <= 10) {							// If the second photon is in the 293 keV interval
									coinc_Tl_01 += 1;										// 10 order Bi event
								}
							}
						}
					}
					else if (abs(e0 - mean2_Tl_0) <= 10) {									// Energy is in 293 keV interval --> Look for 807 keV second photon
						for (Int_t j = -10; j < 10; j++) {									// Check -10 to +10 events
							mytree->GetEntry(i + j + k * entry_perpoint);
							t1 = time;

							if (t1 > t0) {
								dt = t1 - t0;
							}
							else {
								dt = t0 - t1;
							}

							if ((channel == 1) and (dt <= window)) {						// If the second photon is in coincidence and in detector 1
								e1 = energy;
								if (abs(e1 - mean1_Tl_1) <= 10) {							// If the second photon is in the 293 keV interval
									coinc_Tl_10 += 1;										// 10 order Bi event
								}
							}
						}
					}
				}
			}

			cout << "Got coincidences" << endl;

			Double_t Bi_corr = 1.00355*173 / 0.978;													// Branching, Bateman and intensity correction
			Double_t Bi_corr_relerr = sqrt((14 / 173) * (14 / 173) + (0.1 / 97.8) * (0.1 / 97.8) + (20/100355) * (20 / 100355));
			Double_t Tl_corr = 1.00370 / 0.022;
			Double_t Tl_corr_relerr = sqrt((0.02 / 1) * (0.02 / 1) + (0.1 / 2.2) * (0.1 / 2.2) + (33 / 100370) * (33 / 100370));

			Double_t Bi_N1 = (N1_Bi_0 + N1_Bi_1) / 2;											// Total counts
			Double_t Bi_N2 = (N2_Bi_0 + N2_Bi_1) / 2;
			Double_t Bi_N12 = (coinc_Bi_01 + coinc_Bi_10) / 2;
			Double_t Tl_N1 = (N1_Tl_0 + N1_Tl_1) / 2;
			Double_t Tl_N2 = (N2_Tl_0 + N2_Tl_1) / 2;
			Double_t Tl_N12 = (coinc_Tl_01 + coinc_Tl_10) / 2;

			ULong64_t measurement_time;														// Length of measurement
			ULong64_t final_time;
			ULong64_t initial_time;
			mytree->GetEntry(k * entry_perpoint);
			initial_time = time / 1e12;

			if (k == num_points - 1) {
				mytree->GetEntry(entry-1);
			}
			else {
				mytree->GetEntry(entry_perpoint* (k + 1));
			}
			
			final_time = time / 1e12;
			measurement_time = final_time - initial_time;

			cout << "Measured for " << measurement_time << endl;

			Double_t A_Bi = (0.001 * Bi_corr / measurement_time) * Bi_N1 * Bi_N2 / Bi_N12;		// Activity for data point
			Double_t A_Tl = (0.001 * Tl_corr / measurement_time) * Tl_N1 * Tl_N2 / Tl_N12;
			Double_t A_err_Bi = sqrt(Bi_corr_relerr* Bi_corr_relerr + 1/Bi_N12);
			Double_t A_err_Tl = sqrt(Tl_corr_relerr* Tl_corr_relerr + 1/Tl_N12);


			cout << "Bi activity is " << A_Bi << endl;
			cout << "Tl activity is " << A_Tl << endl;
			cout << "Bi error is " << A_err_Bi * 100 << "%" << endl;
			cout << "Tl error is " << A_err_Tl * 100 << "%" << endl;

			//TString file_column = "M120_6";
			myFile << this_dir << ';' << initial_time << ";" << measurement_time << ";" << A_Bi << ";" << A_err_Bi << ";" << A_Tl << ";" << A_err_Tl << endl;
		}
		
	}
	
	return 0;
	}